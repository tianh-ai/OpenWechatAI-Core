#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业通信统一MCP服务器
集成企业微信、飞书、钉钉三大平台
支持配置管理、消息接收、自动回复
"""

from flask import Flask, request, jsonify
import json
import os
import yaml
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enterprise_comm_mcp.feishu_bot import FeishuWebhookBot, FeishuAppBot
from enterprise_comm_mcp.dingtalk_bot import DingTalkWebhookBot, DingTalkAppBot
from wework_bot import WeWorkBot, WeWorkWebhookBot

app = Flask(__name__)

# 配置文件路径
CONFIG_FILE = 'enterprise_comm_mcp/config.yaml'

# 全局配置和机器人实例
config = {}
bots = {}


def load_config():
    """加载配置文件"""
    global config, bots
    
    if not os.path.exists(CONFIG_FILE):
        print("⚠️  配置文件不存在，使用默认配置")
        return
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("✓ 配置文件加载成功")
        print(f"  - 企业微信: {'启用' if config.get('wework', {}).get('enabled') else '禁用'}")
        print(f"  - 飞书: {'启用' if config.get('feishu', {}).get('enabled') else '禁用'}")
        print(f"  - 钉钉: {'启用' if config.get('dingtalk', {}).get('enabled') else '禁用'}")
        
        # 初始化机器人实例
        init_bots()
        
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")


def save_config():
    """保存配置到文件"""
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        print("✓ 配置已保存")
        return True
    except Exception as e:
        print(f"❌ 配置保存失败: {e}")
        return False


def init_bots():
    """根据配置初始化机器人实例"""
    global bots
    bots = {}
    
    # 企业微信
    wework_config = config.get('wework', {})
    if wework_config.get('enabled'):
        if wework_config.get('type') == 'webhook':
            bots['wework'] = WeWorkWebhookBot(wework_config.get('webhook_url'))
        elif wework_config.get('type') == 'app':
            bots['wework'] = WeWorkBot(
                corpid=wework_config.get('corp_id'),
                corpsecret=wework_config.get('corp_secret'),
                agentid=wework_config.get('agent_id')
            )
        print("✓ 企业微信机器人已初始化")
    
    # 飞书
    feishu_config = config.get('feishu', {})
    if feishu_config.get('enabled'):
        if feishu_config.get('type') == 'webhook':
            bots['feishu'] = FeishuWebhookBot(
                webhook_url=feishu_config.get('webhook_url'),
                secret=feishu_config.get('secret')
            )
        elif feishu_config.get('type') == 'app':
            bots['feishu'] = FeishuAppBot(
                app_id=feishu_config.get('app_id'),
                app_secret=feishu_config.get('app_secret')
            )
        print("✓ 飞书机器人已初始化")
    
    # 钉钉
    dingtalk_config = config.get('dingtalk', {})
    if dingtalk_config.get('enabled'):
        if dingtalk_config.get('type') == 'webhook':
            bots['dingtalk'] = DingTalkWebhookBot(
                webhook_url=dingtalk_config.get('webhook_url'),
                secret=dingtalk_config.get('secret')
            )
        elif dingtalk_config.get('type') == 'app':
            bots['dingtalk'] = DingTalkAppBot(
                app_key=dingtalk_config.get('app_key'),
                app_secret=dingtalk_config.get('app_secret')
            )
        print("✓ 钉钉机器人已初始化")


# ==================== 配置管理API ====================

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取当前配置"""
    return jsonify({
        'success': True,
        'data': config
    })


@app.route('/api/config', methods=['POST'])
def update_config():
    """更新配置"""
    global config
    
    try:
        new_config = request.json
        config.update(new_config)
        
        if save_config():
            init_bots()  # 重新初始化机器人
            return jsonify({
                'success': True,
                'message': '配置更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置保存失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'配置更新失败: {str(e)}'
        }), 400


@app.route('/api/config/<platform>', methods=['GET'])
def get_platform_config(platform):
    """获取指定平台配置"""
    if platform not in ['wework', 'feishu', 'dingtalk']:
        return jsonify({
            'success': False,
            'message': '不支持的平台'
        }), 400
    
    return jsonify({
        'success': True,
        'data': config.get(platform, {})
    })


@app.route('/api/config/<platform>', methods=['POST'])
def update_platform_config(platform):
    """更新指定平台配置"""
    if platform not in ['wework', 'feishu', 'dingtalk']:
        return jsonify({
            'success': False,
            'message': '不支持的平台'
        }), 400
    
    try:
        platform_config = request.json
        config[platform] = platform_config
        
        if save_config():
            init_bots()
            return jsonify({
                'success': True,
                'message': f'{platform} 配置更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置保存失败'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'配置更新失败: {str(e)}'
        }), 400


# ==================== 消息发送API ====================

@app.route('/api/send/<platform>', methods=['POST'])
def send_message(platform):
    """发送消息到指定平台"""
    if platform not in bots:
        return jsonify({
            'success': False,
            'message': f'{platform} 未配置或未启用'
        }), 400
    
    try:
        data = request.json
        bot = bots[platform]
        
        # 根据不同平台调用不同方法
        if hasattr(bot, 'send_text'):
            result = bot.send_text(data.get('content'))
        else:
            return jsonify({
                'success': False,
                'message': '该平台不支持发送消息'
            }), 400
        
        return jsonify({
            'success': result,
            'message': '发送成功' if result else '发送失败'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'发送失败: {str(e)}'
        }), 500


# ==================== 消息接收回调 ====================

@app.route('/callback/wework', methods=['GET', 'POST'])
def wework_callback():
    """企业微信消息回调"""
    if 'wework' not in bots:
        return "未配置", 404
    
    bot = bots['wework']
    
    if request.method == 'GET':
        # URL验证
        # 这里需要根据企业微信的验证逻辑实现
        return request.args.get('echostr', '')
    
    elif request.method == 'POST':
        # 处理消息
        # 这里需要解密和解析消息
        if hasattr(bot, 'handle_message'):
            bot.handle_message(request.json)
        return "success"


@app.route('/callback/feishu', methods=['POST'])
def feishu_callback():
    """飞书事件回调"""
    if 'feishu' not in bots:
        return jsonify({'code': -1, 'msg': '未配置'}), 404
    
    try:
        event_data = request.json
        
        # URL验证
        if event_data.get('type') == 'url_verification':
            return jsonify({
                'challenge': event_data.get('challenge')
            })
        
        # 消息事件
        bot = bots['feishu']
        if hasattr(bot, 'handle_message'):
            bot.handle_message(event_data)
        
        return jsonify({'code': 0, 'msg': 'success'})
        
    except Exception as e:
        print(f"❌ 飞书回调处理失败: {e}")
        return jsonify({'code': -1, 'msg': str(e)}), 500


@app.route('/callback/dingtalk', methods=['POST'])
def dingtalk_callback():
    """钉钉消息回调"""
    if 'dingtalk' not in bots:
        return jsonify({'errcode': -1, 'errmsg': '未配置'}), 404
    
    try:
        message_data = request.json
        
        bot = bots['dingtalk']
        if hasattr(bot, 'handle_message'):
            bot.handle_message(message_data)
        
        return jsonify({'errcode': 0, 'errmsg': 'success'})
        
    except Exception as e:
        print(f"❌ 钉钉回调处理失败: {e}")
        return jsonify({'errcode': -1, 'errmsg': str(e)}), 500


# ==================== 健康检查和状态 ====================

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': 'enterprise_comm_mcp',
        'platforms': {
            'wework': 'wework' in bots,
            'feishu': 'feishu' in bots,
            'dingtalk': 'dingtalk' in bots
        }
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    return jsonify({
        'success': True,
        'data': {
            'platforms': {
                'wework': {
                    'enabled': config.get('wework', {}).get('enabled', False),
                    'type': config.get('wework', {}).get('type'),
                    'initialized': 'wework' in bots
                },
                'feishu': {
                    'enabled': config.get('feishu', {}).get('enabled', False),
                    'type': config.get('feishu', {}).get('type'),
                    'initialized': 'feishu' in bots
                },
                'dingtalk': {
                    'enabled': config.get('dingtalk', {}).get('enabled', False),
                    'type': config.get('dingtalk', {}).get('type'),
                    'initialized': 'dingtalk' in bots
                }
            }
        }
    })


if __name__ == "__main__":
    print("="*60)
    print("🤖 企业通信统一MCP服务器")
    print("="*60)
    
    # 加载配置
    load_config()
    
    print("\n="*60)
    print("🚀 服务启动中...")
    print("📌 API 端点:")
    print("  - GET  /api/config           获取所有配置")
    print("  - POST /api/config           更新所有配置")
    print("  - GET  /api/config/<platform> 获取平台配置")
    print("  - POST /api/config/<platform> 更新平台配置")
    print("  - POST /api/send/<platform>   发送消息")
    print("  - GET  /api/status           系统状态")
    print("\n📌 回调端点:")
    print("  - /callback/wework           企业微信回调")
    print("  - /callback/feishu           飞书回调")
    print("  - /callback/dingtalk         钉钉回调")
    print("\n按 Ctrl+C 停止\n")
    
    # 启动服务
    app.run(host='0.0.0.0', port=8000, debug=True)
