#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉机器人 - 基于官方API
支持群机器人和企业内部应用两种方式
"""

import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from reply_rule_engine import ReplyRuleEngine


class DingTalkWebhookBot:
    """钉钉群机器人（Webhook方式）- 仅支持发送"""
    
    def __init__(self, webhook_url, secret=None):
        """
        初始化钉钉群机器人
        
        Args:
            webhook_url: 群机器人的Webhook地址
            secret: 加签密钥（如果启用了加签）
        """
        self.webhook_url = webhook_url
        self.secret = secret
    
    def _gen_sign(self, timestamp):
        """生成签名"""
        if not self.secret:
            return None, None
        
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        
        hmac_code = hmac.new(
            secret_enc,
            string_to_sign_enc,
            digestmod=hashlib.sha256
        ).digest()
        
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign
    
    def _get_webhook_url(self):
        """获取带签名的Webhook URL"""
        if not self.secret:
            return self.webhook_url
        
        timestamp = str(round(time.time() * 1000))
        _, sign = self._gen_sign(timestamp)
        return f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"
    
    def send_text(self, content, at_mobiles=None, is_at_all=False):
        """
        发送文本消息
        
        Args:
            content: 消息内容
            at_mobiles: @的手机号列表
            is_at_all: 是否@所有人
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": is_at_all
            }
        }
        
        try:
            url = self._get_webhook_url()
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                print(f"✓ 钉钉消息发送成功")
                return True
            else:
                print(f"❌ 钉钉发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 钉钉发送异常: {e}")
            return False
    
    def send_markdown(self, title, text, at_mobiles=None, is_at_all=False):
        """发送Markdown消息"""
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": is_at_all
            }
        }
        
        try:
            url = self._get_webhook_url()
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            return result.get('errcode') == 0
        except Exception as e:
            print(f"❌ 钉钉发送异常: {e}")
            return False
    
    def send_link(self, title, text, message_url, pic_url=None):
        """发送链接消息"""
        data = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "messageUrl": message_url,
                "picUrl": pic_url or ""
            }
        }
        
        try:
            url = self._get_webhook_url()
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            return result.get('errcode') == 0
        except Exception as e:
            print(f"❌ 钉钉发送异常: {e}")
            return False
    
    def send_action_card(self, title, text, btns):
        """
        发送ActionCard消息
        
        Args:
            title: 标题
            text: 内容
            btns: 按钮列表 [{"title": "按钮1", "actionURL": "url1"}, ...]
        """
        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "btnOrientation": "0",
                "btns": btns
            }
        }
        
        try:
            url = self._get_webhook_url()
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            return result.get('errcode') == 0
        except Exception as e:
            print(f"❌ 钉钉发送异常: {e}")
            return False


class DingTalkAppBot:
    """钉钉企业内部应用机器人 - 完整功能"""
    
    def __init__(self, app_key, app_secret):
        """
        初始化钉钉应用机器人
        
        Args:
            app_key: 应用的AppKey
            app_secret: 应用的AppSecret
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = None
        self.token_expire_time = 0
        
        # 加载回复规则
        self.rule_engine = ReplyRuleEngine('config/reply_rules.yaml')
        print(f"✓ 已加载 {len(self.rule_engine.rules)} 条规则")
    
    def get_access_token(self):
        """获取access_token"""
        if self.access_token and time.time() < self.token_expire_time - 300:
            return self.access_token
        
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            'appkey': self.app_key,
            'appsecret': self.app_secret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                self.access_token = result['access_token']
                self.token_expire_time = time.time() + result.get('expires_in', 7200)
                print("✓ 钉钉 Access Token 获取成功")
                return self.access_token
            else:
                print(f"❌ 获取Token失败: {result}")
                return None
        except Exception as e:
            print(f"❌ 获取Token异常: {e}")
            return None
    
    def send_work_message(self, user_id_list, msg_body):
        """
        发送工作通知消息
        
        Args:
            user_id_list: 用户ID列表（逗号分隔）
            msg_body: 消息体
        """
        token = self.get_access_token()
        if not token:
            return False
        
        url = f"https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token={token}"
        
        data = {
            "agent_id": self.agent_id,
            "userid_list": user_id_list,
            "msg": msg_body
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                print(f"✓ 钉钉消息发送成功")
                return True
            else:
                print(f"❌ 钉钉发送失败: {result}")
                return False
        except Exception as e:
            print(f"❌ 钉钉发送异常: {e}")
            return False
    
    def send_text_message(self, user_id_list, content):
        """发送文本消息"""
        msg_body = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        return self.send_work_message(user_id_list, msg_body)
    
    def handle_message(self, message_data):
        """
        处理接收到的消息（从回调接口调用）
        
        Args:
            message_data: 钉钉推送的消息数据
        """
        try:
            msg_type = message_data.get('msgtype')
            
            # 只处理文本消息
            if msg_type != 'text':
                print(f"⚠️ 忽略非文本消息: {msg_type}")
                return
            
            sender_id = message_data.get('senderStaffId')
            content = message_data.get('text', {}).get('content', '')
            
            print(f"\n📨 收到钉钉消息: {sender_id} -> {content}")
            
            # 构造消息对象
            msg_obj = {
                'type': 'text',
                'content': content,
                'sender': sender_id,
                'is_self': False
            }
            
            # 匹配回复规则
            reply = self.rule_engine.match_rule(msg_obj)
            
            if reply:
                print(f"💬 自动回复: {reply}")
                self.send_text_message(sender_id, reply)
            else:
                print("⚠️ 未匹配到规则")
                
        except Exception as e:
            print(f"❌ 处理消息失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    print("="*60)
    print("钉钉机器人示例")
    print("="*60)
    
    print("\n【方式1：群机器人 Webhook】")
    print("使用示例：")
    print("""
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookBot(webhook_url, secret="YOUR_SECRET")
    bot.send_text("测试消息")
    bot.send_text("重要通知", at_mobiles=["13800138000"], is_at_all=False)
    """)
    
    print("\n【方式2：企业内部应用】")
    print("使用示例：")
    print("""
    bot = DingTalkAppBot(
        app_key='YOUR_APP_KEY',
        app_secret='YOUR_APP_SECRET'
    )
    bot.send_text_message('user_id', '你好')
    """)
    
    print("\n📚 官方文档：")
    print("https://open.dingtalk.com/document/")
