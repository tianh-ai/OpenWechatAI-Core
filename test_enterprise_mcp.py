#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业通信MCP快速测试脚本
测试各平台的配置和消息发送功能
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """测试服务健康状态"""
    print_section("1. 测试服务健康状态")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        result = response.json()
        print(f"✓ 服务状态: {result['status']}")
        print(f"  平台状态:")
        for platform, status in result['platforms'].items():
            print(f"    - {platform}: {'已初始化' if status else '未初始化'}")
        return True
    except Exception as e:
        print(f"❌ 服务未运行或连接失败: {e}")
        print("\n💡 请先启动服务:")
        print("   cd enterprise_comm_mcp && python mcp_server.py")
        return False

def test_get_config():
    """测试获取配置"""
    print_section("2. 测试获取配置")
    try:
        response = requests.get(f"{API_BASE}/api/config")
        result = response.json()
        if result['success']:
            print("✓ 配置获取成功")
            config = result['data']
            
            # 企业微信
            if 'wework' in config:
                wework = config['wework']
                print(f"\n  企业微信:")
                print(f"    - 启用: {wework.get('enabled', False)}")
                print(f"    - 类型: {wework.get('type', 'N/A')}")
            
            # 飞书
            if 'feishu' in config:
                feishu = config['feishu']
                print(f"\n  飞书:")
                print(f"    - 启用: {feishu.get('enabled', False)}")
                print(f"    - 类型: {feishu.get('type', 'N/A')}")
            
            # 钉钉
            if 'dingtalk' in config:
                dingtalk = config['dingtalk']
                print(f"\n  钉钉:")
                print(f"    - 启用: {dingtalk.get('enabled', False)}")
                print(f"    - 类型: {dingtalk.get('type', 'N/A')}")
            
            return True
        else:
            print(f"❌ 获取失败: {result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_update_config():
    """测试更新配置"""
    print_section("3. 测试更新配置（可选）")
    
    print("\n是否要测试配置更新功能? (y/n): ", end='')
    choice = input().strip().lower()
    
    if choice != 'y':
        print("⏭️  跳过配置更新测试")
        return True
    
    print("\n选择要配置的平台:")
    print("1) 企业微信")
    print("2) 飞书")
    print("3) 钉钉")
    print("0) 跳过")
    
    platform_choice = input("请选择 (0-3): ").strip()
    
    if platform_choice == '0':
        print("⏭️  跳过")
        return True
    
    platform_map = {
        '1': 'wework',
        '2': 'feishu',
        '3': 'dingtalk'
    }
    
    platform = platform_map.get(platform_choice)
    if not platform:
        print("❌ 无效选择")
        return False
    
    print(f"\n配置 {platform}:")
    print("选择类型: 1) webhook  2) app")
    type_choice = input("请选择 (1-2): ").strip()
    
    config_type = 'webhook' if type_choice == '1' else 'app'
    
    new_config = {
        'enabled': True,
        'type': config_type
    }
    
    if config_type == 'webhook':
        webhook_url = input("输入Webhook URL: ").strip()
        new_config['webhook_url'] = webhook_url
        
        if platform in ['feishu', 'dingtalk']:
            secret = input("输入Secret (可选，直接回车跳过): ").strip()
            if secret:
                new_config['secret'] = secret
    else:
        print("⚠️  应用模式需要更多配置，建议使用Web界面配置")
        return True
    
    try:
        response = requests.post(
            f"{API_BASE}/api/config/{platform}",
            json=new_config
        )
        result = response.json()
        
        if result['success']:
            print(f"✓ {platform} 配置更新成功")
            return True
        else:
            print(f"❌ 更新失败: {result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_send_message():
    """测试发送消息"""
    print_section("4. 测试发送消息")
    
    # 获取当前配置
    try:
        response = requests.get(f"{API_BASE}/api/status")
        status = response.json()
        
        enabled_platforms = []
        for platform, info in status['data']['platforms'].items():
            if info['enabled'] and info['initialized']:
                enabled_platforms.append(platform)
        
        if not enabled_platforms:
            print("⚠️  没有已启用的平台，无法测试发送")
            print("   请先配置至少一个平台")
            return True
        
        print(f"\n已启用的平台: {', '.join(enabled_platforms)}")
        print("\n选择要测试的平台:")
        for i, platform in enumerate(enabled_platforms, 1):
            print(f"{i}) {platform}")
        print("0) 跳过")
        
        choice = input(f"请选择 (0-{len(enabled_platforms)}): ").strip()
        
        if choice == '0':
            print("⏭️  跳过发送测试")
            return True
        
        try:
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= len(enabled_platforms):
                print("❌ 无效选择")
                return False
            
            platform = enabled_platforms[choice_idx]
            
            message = f"测试消息 - {time.strftime('%Y-%m-%d %H:%M:%S')}"
            print(f"\n发送测试消息到 {platform}...")
            print(f"内容: {message}")
            
            response = requests.post(
                f"{API_BASE}/api/send/{platform}",
                json={'content': message}
            )
            result = response.json()
            
            if result['success']:
                print(f"✓ 消息发送成功！")
                print("  请检查对应平台是否收到消息")
                return True
            else:
                print(f"❌ 发送失败: {result.get('message')}")
                return False
                
        except ValueError:
            print("❌ 无效输入")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    print("="*60)
    print("  🤖 企业通信MCP - 快速测试")
    print("="*60)
    print("\n本脚本将测试:")
    print("  1. 服务健康状态")
    print("  2. 配置获取")
    print("  3. 配置更新（可选）")
    print("  4. 消息发送（可选）")
    print("\n开始测试...\n")
    
    # 测试1: 健康检查
    if not test_health():
        return
    
    time.sleep(1)
    
    # 测试2: 获取配置
    if not test_get_config():
        print("\n⚠️  配置获取失败，但继续测试...")
    
    time.sleep(1)
    
    # 测试3: 更新配置
    test_update_config()
    
    time.sleep(1)
    
    # 测试4: 发送消息
    test_send_message()
    
    # 总结
    print_section("测试完成")
    print("\n💡 下一步:")
    print("  1. 如果测试失败，请检查配置")
    print("  2. 使用Web界面进行可视化配置:")
    print("     http://localhost:8000/static/config.html")
    print("  3. 查看详细文档:")
    print("     enterprise_comm_mcp/README.md")
    print("\n✓ 测试结束\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  测试中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
