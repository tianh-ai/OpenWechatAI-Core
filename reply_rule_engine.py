#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能回复规则引擎
"""

import yaml
import re
from datetime import datetime
import os

class ReplyRuleEngine:
    def __init__(self, config_path="config/reply_rules.yaml"):
        self.config_path = config_path
        self.rules = []
        self.default_reply = None
        self.blacklist = []
        self.whitelist = []
        
        self.load_rules()
    
    def load_rules(self):
        """加载规则配置"""
        if not os.path.exists(self.config_path):
            print(f"⚠️  规则配置文件不存在: {self.config_path}")
            return
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            self.rules = config.get('rules', [])
            self.default_reply = config.get('default_reply', {})
            self.blacklist = config.get('blacklist', [])
            self.whitelist = config.get('whitelist', [])
            
            print(f"✓ 已加载 {len(self.rules)} 条规则")
        
        except Exception as e:
            print(f"❌ 加载规则失败: {e}")
    
    def reload_rules(self):
        """重新加载规则（支持热更新）"""
        print("🔄 重新加载规则...")
        self.load_rules()
    
    def check_time_condition(self, time_range):
        """检查时间条件"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        
        for tr in time_range:
            start = tr.get('start', '00:00')
            end = tr.get('end', '23:59')
            
            # 跨天情况（如 22:00 - 08:00）
            if start > end:
                if current_time >= start or current_time <= end:
                    return True
            else:
                if start <= current_time <= end:
                    return True
        
        return False
    
    def check_weekday_condition(self, weekdays):
        """检查星期条件（1=周一, 7=周日）"""
        current_weekday = datetime.now().isoweekday()
        return current_weekday in weekdays
    
    def check_keyword_condition(self, message_content, keywords):
        """检查关键词条件"""
        for kw in keywords:
            pattern = kw.get('pattern', '')
            if re.search(pattern, message_content, re.IGNORECASE):
                return kw.get('reply')
        return None
    
    def check_contact_condition(self, contact_name, contacts):
        """检查联系人条件"""
        return contact_name in contacts
    
    def check_message_type_condition(self, message_type, required_type):
        """检查消息类型条件"""
        return message_type == required_type
    
    def match_rule(self, message_info, contact_name=None):
        """
        匹配规则并返回回复
        
        Args:
            message_info: 消息信息 dict
                - type: 消息类型 (text/voice/image)
                - content: 消息内容
            contact_name: 联系人名称
        
        Returns:
            str: 回复内容，None 表示不回复
        """
        # 检查黑名单
        if contact_name and contact_name in self.blacklist:
            print(f"⛔ 联系人 '{contact_name}' 在黑名单中，不回复")
            return None
        
        message_type = message_info.get('type', 'unknown')
        message_content = message_info.get('content', '')
        
        # 遍历规则
        for rule in self.rules:
            if not rule.get('enabled', True):
                continue
            
            rule_name = rule.get('name', 'Unknown')
            conditions = rule.get('conditions', {})
            
            # 检查所有条件
            all_conditions_met = True
            keyword_reply = None
            
            # 时间条件
            if 'time_range' in conditions:
                if not self.check_time_condition(conditions['time_range']):
                    all_conditions_met = False
            
            # 星期条件
            if 'weekdays' in conditions:
                if not self.check_weekday_condition(conditions['weekdays']):
                    all_conditions_met = False
            
            # 关键词条件
            if 'keywords' in conditions:
                keyword_reply = self.check_keyword_condition(message_content, conditions['keywords'])
                if keyword_reply is None:
                    all_conditions_met = False
            
            # 联系人条件
            if 'contacts' in conditions and contact_name:
                if not self.check_contact_condition(contact_name, conditions['contacts']):
                    all_conditions_met = False
            
            # 消息类型条件
            if 'message_type' in conditions:
                if not self.check_message_type_condition(message_type, conditions['message_type']):
                    all_conditions_met = False
            
            # 所有条件满足
            if all_conditions_met:
                print(f"✓ 匹配规则: {rule_name}")
                
                # 如果有关键词匹配的特定回复，优先使用
                if keyword_reply:
                    return keyword_reply
                
                # 否则使用规则的 actions
                actions = rule.get('actions', [])
                for action in actions:
                    if action.get('type') == 'reply':
                        return action.get('message')
        
        # 没有规则匹配，使用默认回复
        if self.default_reply.get('enabled', False):
            print("ℹ️  使用默认回复")
            return self.default_reply.get('message')
        
        return None

if __name__ == "__main__":
    # 测试规则引擎
    engine = ReplyRuleEngine()
    
    # 测试用例
    test_cases = [
        {
            "message": {"type": "text", "content": "你好"},
            "contact": "测试用户",
            "expected": "包含'你好'"
        },
        {
            "message": {"type": "text", "content": "价格多少"},
            "contact": "客户A",
            "expected": "价格信息"
        },
        {
            "message": {"type": "voice", "content": "[语音]"},
            "contact": "用户B",
            "expected": "语音消息"
        },
        {
            "message": {"type": "text", "content": "随机消息"},
            "contact": "路人",
            "expected": "默认回复"
        },
    ]
    
    print("="*60)
    print("规则引擎测试")
    print("="*60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[测试 {i}]")
        print(f"  消息: {test['message']}")
        print(f"  联系人: {test['contact']}")
        
        reply = engine.match_rule(test['message'], test['contact'])
        print(f"  回复: {reply}")
        print(f"  预期: {test['expected']}")
