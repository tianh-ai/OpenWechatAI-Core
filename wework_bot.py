#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信机器人 - 基于官方API
完全不需要手机，通过HTTP接口收发消息
"""

import requests
import json
import time
from reply_rule_engine import ReplyRuleEngine

class WeWorkBot:
    """企业微信应用机器人"""
    
    def __init__(self, corpid, corpsecret, agentid):
        """
        初始化企业微信机器人
        
        Args:
            corpid: 企业ID
            corpsecret: 应用的Secret
            agentid: 应用ID
        """
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = None
        self.token_expire_time = 0
        
        # 加载回复规则
        self.rule_engine = ReplyRuleEngine('config/reply_rules.yaml')
        print(f"✓ 已加载 {len(self.rule_engine.rules)} 条规则")
    
    def get_access_token(self):
        """获取access_token"""
        # Token有效期7200秒，提前5分钟刷新
        if self.access_token and time.time() < self.token_expire_time - 300:
            return self.access_token
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                self.access_token = result['access_token']
                self.token_expire_time = time.time() + result.get('expires_in', 7200)
                print("✓ Access Token 获取成功")
                return self.access_token
            else:
                print(f"❌ 获取Token失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 获取Token异常: {e}")
            return None
    
    def send_text_message(self, user_id, content):
        """
        发送文本消息
        
        Args:
            user_id: 用户ID（成员ID），@all 表示全部成员
            content: 消息内容
        """
        token = self.get_access_token()
        if not token:
            return False
        
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
        
        data = {
            "touser": user_id,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": content
            },
            "safe": 0
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                print(f"✓ 消息发送成功: {content[:20]}...")
                return True
            else:
                print(f"❌ 消息发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 发送异常: {e}")
            return False
    
    def handle_message(self, message_data):
        """
        处理接收到的消息（从回调接口调用）
        
        Args:
            message_data: 企业微信推送的消息数据
        """
        try:
            # 解析消息
            msg_type = message_data.get('MsgType')
            from_user = message_data.get('FromUserName')
            
            # 只处理文本消息
            if msg_type != 'text':
                print(f"⚠️ 忽略非文本消息: {msg_type}")
                return
            
            content = message_data.get('Content', '')
            
            print(f"\n📨 收到消息: {from_user} -> {content}")
            
            # 构造消息对象
            msg_obj = {
                'type': 'text',
                'content': content,
                'sender': from_user,
                'is_self': False
            }
            
            # 匹配回复规则
            reply = self.rule_engine.match_rule(msg_obj)
            
            if reply:
                print(f"💬 自动回复: {reply}")
                self.send_text_message(from_user, reply)
            else:
                print("⚠️ 未匹配到规则")
                
        except Exception as e:
            print(f"❌ 处理消息失败: {e}")
            import traceback
            traceback.print_exc()


class WeWorkWebhookBot:
    """企业微信群机器人（Webhook方式）- 仅支持发送"""
    
    def __init__(self, webhook_url):
        """
        初始化群机器人
        
        Args:
            webhook_url: 群机器人的Webhook地址
        """
        self.webhook_url = webhook_url
    
    def send_text(self, content, mentioned_list=None):
        """
        发送文本消息到群
        
        Args:
            content: 消息内容
            mentioned_list: @的成员列表，如 ["userid1", "userid2"]，@all 表示提醒所有人
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        if mentioned_list:
            data["text"]["mentioned_list"] = mentioned_list
        
        try:
            response = requests.post(self.webhook_url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                print(f"✓ 消息发送成功")
                return True
            else:
                print(f"❌ 发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 发送异常: {e}")
            return False
    
    def send_markdown(self, content):
        """发送Markdown消息"""
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        
        try:
            response = requests.post(self.webhook_url, json=data, timeout=10)
            result = response.json()
            return result.get('errcode') == 0
        except Exception as e:
            print(f"❌ 发送异常: {e}")
            return False


if __name__ == "__main__":
    print("="*60)
    print("企业微信机器人示例")
    print("="*60)
    
    # 示例1: 群机器人（Webhook）
    print("\n【方式1：群机器人 - 仅发送消息】")
    print("1. 在企业微信群中添加机器人")
    print("2. 获取Webhook地址")
    print("3. 使用示例：")
    print("""
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    bot = WeWorkWebhookBot(webhook_url)
    bot.send_text("测试消息")
    """)
    
    # 示例2: 应用机器人
    print("\n【方式2：应用机器人 - 完整功能】")
    print("1. 登录企业微信管理后台")
    print("2. 创建应用，获取 AgentId 和 Secret")
    print("3. 获取企业ID（CorpId）")
    print("4. 配置接收消息的回调URL")
    print("5. 使用示例：")
    print("""
    bot = WeWorkBot(
        corpid='YOUR_CORP_ID',
        corpsecret='YOUR_SECRET',
        agentid='YOUR_AGENT_ID'
    )
    bot.send_text_message('userid', '你好')
    """)
    
    print("\n💡 推荐：")
    print("- 仅需发送通知 → 使用群机器人（Webhook）")
    print("- 需要自动回复 → 使用应用机器人 + 回调服务器")
    print("\n📚 官方文档：")
    print("https://developer.work.weixin.qq.com/document/path/90664")
