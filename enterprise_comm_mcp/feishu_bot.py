#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书机器人 - 基于官方API
支持群机器人和自建应用两种方式
"""

import requests
import json
import time
import hmac
import hashlib
import base64
from reply_rule_engine import ReplyRuleEngine


class FeishuWebhookBot:
    """飞书群机器人（Webhook方式）- 仅支持发送"""
    
    def __init__(self, webhook_url, secret=None):
        """
        初始化飞书群机器人
        
        Args:
            webhook_url: 群机器人的Webhook地址
            secret: 签名密钥（如果启用了签名校验）
        """
        self.webhook_url = webhook_url
        self.secret = secret
    
    def _gen_sign(self, timestamp):
        """生成签名"""
        if not self.secret:
            return None
        
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign
    
    def send_text(self, content):
        """发送文本消息"""
        timestamp = str(int(time.time()))
        data = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        
        if self.secret:
            data["timestamp"] = timestamp
            data["sign"] = self._gen_sign(timestamp)
        
        try:
            response = requests.post(self.webhook_url, json=data, timeout=10)
            result = response.json()
            
            if result.get('StatusCode') == 0:
                print(f"✓ 飞书消息发送成功")
                return True
            else:
                print(f"❌ 飞书发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 飞书发送异常: {e}")
            return False
    
    def send_rich_text(self, title, content):
        """发送富文本消息"""
        timestamp = str(int(time.time()))
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [[{"tag": "text", "text": content}]]
                    }
                }
            }
        }
        
        if self.secret:
            data["timestamp"] = timestamp
            data["sign"] = self._gen_sign(timestamp)
        
        try:
            response = requests.post(self.webhook_url, json=data, timeout=10)
            result = response.json()
            return result.get('StatusCode') == 0
        except Exception as e:
            print(f"❌ 飞书发送异常: {e}")
            return False
    
    def send_card(self, title, content):
        """发送卡片消息"""
        timestamp = str(int(time.time()))
        data = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": content
                        }
                    }
                ]
            }
        }
        
        if self.secret:
            data["timestamp"] = timestamp
            data["sign"] = self._gen_sign(timestamp)
        
        try:
            response = requests.post(self.webhook_url, json=data, timeout=10)
            result = response.json()
            return result.get('StatusCode') == 0
        except Exception as e:
            print(f"❌ 飞书发送异常: {e}")
            return False


class FeishuAppBot:
    """飞书自建应用机器人 - 完整功能"""
    
    def __init__(self, app_id, app_secret):
        """
        初始化飞书应用机器人
        
        Args:
            app_id: 应用ID
            app_secret: 应用Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None
        self.token_expire_time = 0
        
        # 加载回复规则
        self.rule_engine = ReplyRuleEngine('config/reply_rules.yaml')
        print(f"✓ 已加载 {len(self.rule_engine.rules)} 条规则")
    
    def get_tenant_access_token(self):
        """获取tenant_access_token"""
        if self.tenant_access_token and time.time() < self.token_expire_time - 300:
            return self.tenant_access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('code') == 0:
                self.tenant_access_token = result['tenant_access_token']
                self.token_expire_time = time.time() + result.get('expire', 7200)
                print("✓ 飞书 Access Token 获取成功")
                return self.tenant_access_token
            else:
                print(f"❌ 获取Token失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 获取Token异常: {e}")
            return None
    
    def send_message(self, receive_id, msg_type, content, receive_id_type="open_id"):
        """
        发送消息
        
        Args:
            receive_id: 接收者ID
            msg_type: 消息类型 (text, post, image, etc.)
            content: 消息内容
            receive_id_type: ID类型 (open_id, user_id, email, chat_id)
        """
        token = self.get_tenant_access_token()
        if not token:
            return False
        
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps(content) if isinstance(content, dict) else content
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if result.get('code') == 0:
                print(f"✓ 飞书消息发送成功")
                return True
            else:
                print(f"❌ 飞书发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 飞书发送异常: {e}")
            return False
    
    def send_text(self, receive_id, text, receive_id_type="open_id"):
        """发送文本消息"""
        content = {"text": text}
        return self.send_message(receive_id, "text", content, receive_id_type)
    
    def handle_message(self, event_data):
        """
        处理接收到的消息（从事件回调调用）
        
        Args:
            event_data: 飞书推送的事件数据
        """
        try:
            event = event_data.get('event', {})
            msg_type = event.get('message', {}).get('message_type')
            
            # 只处理文本消息
            if msg_type != 'text':
                print(f"⚠️ 忽略非文本消息: {msg_type}")
                return
            
            sender_id = event.get('sender', {}).get('sender_id', {}).get('open_id')
            content = json.loads(event.get('message', {}).get('content', '{}'))
            text = content.get('text', '')
            
            print(f"\n📨 收到飞书消息: {sender_id} -> {text}")
            
            # 构造消息对象
            msg_obj = {
                'type': 'text',
                'content': text,
                'sender': sender_id,
                'is_self': False
            }
            
            # 匹配回复规则
            reply = self.rule_engine.match_rule(msg_obj)
            
            if reply:
                print(f"💬 自动回复: {reply}")
                self.send_text(sender_id, reply)
            else:
                print("⚠️ 未匹配到规则")
                
        except Exception as e:
            print(f"❌ 处理消息失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("飞书机器人示例")
    print("="*60)
    
    print("\n【方式1：群机器人 Webhook】")
    print("使用示例：")
    print("""
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookBot(webhook_url, secret="YOUR_SECRET")
    bot.send_text("测试消息")
    """)
    
    print("\n【方式2：自建应用机器人】")
    print("使用示例：")
    print("""
    bot = FeishuAppBot(
        app_id='YOUR_APP_ID',
        app_secret='YOUR_APP_SECRET'
    )
    bot.send_text('open_id_xxx', '你好')
    """)
    
    print("\n📚 官方文档：")
    print("https://open.feishu.cn/document/home/index")
