#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信自动回复服务器
基于Flask接收企业微信消息回调，自动回复

不需要手机！纯API方式！
"""

from flask import Flask, request
from wework_bot import WeWorkBot
import xml.etree.ElementTree as ET
from WXBizMsgCrypt3 import WXBizMsgCrypt
import os

app = Flask(__name__)

# 企业微信配置（从环境变量读取）
CORP_ID = os.getenv('WEWORK_CORP_ID', '')
CORP_SECRET = os.getenv('WEWORK_CORP_SECRET', '')
AGENT_ID = os.getenv('WEWORK_AGENT_ID', '')
TOKEN = os.getenv('WEWORK_TOKEN', '')  # 回调Token
ENCODING_AES_KEY = os.getenv('WEWORK_ENCODING_AES_KEY', '')  # 回调加密密钥

# 初始化机器人
bot = WeWorkBot(CORP_ID, CORP_SECRET, AGENT_ID)

# 初始化加密库
wxcpt = WXBizMsgCrypt(TOKEN, ENCODING_AES_KEY, CORP_ID)


@app.route('/wework/callback', methods=['GET', 'POST'])
def wework_callback():
    """企业微信消息回调接口"""
    
    if request.method == 'GET':
        # 验证URL有效性
        msg_signature = request.args.get('msg_signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        ret, sEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        if ret != 0:
            return "验证失败", 403
        return sEchoStr
    
    elif request.method == 'POST':
        # 接收并处理消息
        msg_signature = request.args.get('msg_signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        
        # 解密消息
        ret, sMsg = wxcpt.DecryptMsg(
            request.data,
            msg_signature,
            timestamp,
            nonce
        )
        
        if ret != 0:
            print(f"❌ 解密失败: {ret}")
            return "解密失败", 400
        
        # 解析XML消息
        try:
            xml_tree = ET.fromstring(sMsg)
            message_data = {}
            for child in xml_tree:
                message_data[child.tag] = child.text
            
            # 处理消息（自动回复）
            bot.handle_message(message_data)
            
        except Exception as e:
            print(f"❌ 处理消息失败: {e}")
            import traceback
            traceback.print_exc()
        
        return "success"


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return {"status": "ok", "service": "wework_auto_reply"}


if __name__ == "__main__":
    print("="*60)
    print("🤖 企业微信自动回复服务器")
    print("="*60)
    print(f"📱 企业ID: {CORP_ID[:10]}...")
    print(f"🔧 应用ID: {AGENT_ID}")
    print(f"📝 已加载规则: {len(bot.rule_engine.rules)}")
    print("="*60)
    print("\n🚀 服务启动中...")
    print("📌 回调URL: http://your-domain.com/wework/callback")
    print("\n💡 使用说明：")
    print("1. 配置环境变量（WEWORK_CORP_ID等）")
    print("2. 在企业微信后台配置回调URL")
    print("3. 用户发送消息 → 企业微信推送到此服务器 → 自动回复")
    print("\n按 Ctrl+C 停止\n")
    
    # 生产环境使用 gunicorn 或 uwsgi
    app.run(host='0.0.0.0', port=5000, debug=False)
