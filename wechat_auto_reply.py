#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信自动回复系统
整合发送和接收功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from wechat_sender import WeChatSender
from wechat_receiver import WeChatReceiver
from message_ocr import MessageOCR
from reply_rule_engine import ReplyRuleEngine
import time

class WeChatAutoReply:
    def __init__(self, use_ocr=False, ocr_engine="paddle", use_rules=True):
        self.sender = WeChatSender()
        self.receiver = WeChatReceiver()
        self.running = False
        
        # 保持屏幕常亮
        self._keep_screen_on()
        
        # 已回复消息记录（用于去重）
        self.replied_messages = set()  # 存储已回复消息的hash
        self.last_message_content = ""  # 上一条消息内容
        
        # OCR 支持
        self.use_ocr = use_ocr
        self.ocr = None
        if use_ocr:
            try:
                self.ocr = MessageOCR(ocr_engine=ocr_engine)
                print(f"✓ OCR 已启用 (引擎: {ocr_engine})")
            except Exception as e:
                print(f"⚠️  OCR 初始化失败: {e}")
                print("   将使用无 OCR 模式")
                self.use_ocr = False
        
        # 规则引擎
        self.use_rules = use_rules
        self.rule_engine = None
        if use_rules:
            try:
                self.rule_engine = ReplyRuleEngine()
                print(f"✓ 规则引擎已启用")
            except Exception as e:
                print(f"⚠️  规则引擎初始化失败: {e}")
                self.use_rules = False
    
    def _keep_screen_on(self):
        """保持屏幕常亮并解锁"""
        try:
            import subprocess
            # 唤醒屏幕
            subprocess.run(['adb', 'shell', 'input', 'keyevent', '26'], 
                         capture_output=True, timeout=3, check=False)
            time.sleep(0.3)
            
            # 解锁屏幕 (按菜单键)
            subprocess.run(['adb', 'shell', 'input', 'keyevent', '82'], 
                         capture_output=True, timeout=3, check=False)
            time.sleep(0.3)
            
            # 上滑解锁
            subprocess.run(['adb', 'shell', 'input', 'swipe', '540', '2000', '540', '500'], 
                         capture_output=True, timeout=3, check=False)
            time.sleep(0.5)
            
            # 保持屏幕常亮
            subprocess.run(['adb', 'shell', 'svc', 'power', 'stayon', 'true'], 
                         capture_output=True, timeout=3, check=False)
            
            # 禁用自动锁屏
            subprocess.run(['adb', 'shell', 'settings', 'put', 'system', 'screen_off_timeout', '2147483647'], 
                         capture_output=True, timeout=3, check=False)
            
            print("✓ 屏幕已解锁并保持常亮")
        except Exception as e:
            print(f"⚠️  无法解锁屏幕: {e}")
        
    def simple_reply_rule(self, message_screenshot):
        """
        简单的回复规则（暂时返回固定回复）
        后续可以集成OCR和AI
        
        Args:
            message_screenshot: 消息截图路径
        
        Returns:
            str: 回复内容，None表示不回复
        """
        # TODO: 集成OCR识别消息内容
        # TODO: 集成AI生成回复
        
        return "收到，我是自动回复"
    
    def start_monitoring(self, reply_rule=None, check_interval=3):
        """
        开始监控并自动回复
        
        Args:
            reply_rule: 自定义回复规则函数
            check_interval: 检查间隔（秒）
        """
        if reply_rule is None:
            reply_rule = self.simple_reply_rule
        
        self.running = True
        
        print("="*60)
        print("🤖 微信自动回复系统已启动")
        print("="*60)
        print(f"\n📱 设备: {self.sender.width}x{self.sender.height}")
        print(f"⏱️  检查间隔: {check_interval}秒")
        print("\n按 Ctrl+C 停止\n")
        
        # 初始化
        self.receiver._has_new_message()
        
        message_count = 0
        
        try:
            while self.running:
                time.sleep(check_interval)
                
                # 检测新消息
                if not self.receiver._has_new_message():
                    continue
                
                message_count += 1
                print(f"\n[消息 #{message_count}] ✉️  收到新消息！")
                
                # 先点击进入聊天窗口
                try:
                    self.receiver.click_latest_chat_with_red_dot()
                except Exception as e:
                    print(f"  ⚠️  进入聊天窗口失败: {e}")
                
                # 截图
                try:
                    msg_path = self.receiver.get_latest_message_screenshot(
                        f"screenshots/auto_reply/msg_{message_count}.jpg"
                    )
                    print(f"  📸 截图: {msg_path}")
                except Exception as e:
                    print(f"  ❌ 截图失败: {e}")
                    continue
                
                # 使用 OCR 识别消息内容
                message_info = None
                
                if self.use_ocr and self.ocr:
                    try:
                        print(f"  🔍 OCR识别中...")
                        message_info = self.ocr.extract_latest_message(msg_path)
                        
                        if message_info and message_info.get('content'):
                            msg_content = message_info['content']
                            print(f"  📝 内容: {msg_content}")
                            
                            # 简单去重：检查是否包含自己的回复特征
                            if "收到" in msg_content and "消息" in msg_content:
                                print(f"  ⏭️  跳过自己的回复")
                                continue
                        else:
                            print(f"  ⚠️  OCR未识别到内容")
                            
                    except Exception as e:
                        print(f"  ⚠️  OCR失败: {e}")
                    
                    # 生成回复
                    print(f"  🤔 准备生成回复...")
                    if message_info:
                        # 使用规则引擎
                        if self.use_rules and self.rule_engine:
                            reply = self.rule_engine.match_rule(message_info)
                        else:
                            reply = reply_rule(message_info)
                    else:
                        reply = reply_rule(msg_path)  # 降级到使用截图路径
                    
                    if reply:
                        print(f"  💬 回复: {reply}")
                        
                        # 发送回复
                        time.sleep(1)  # 稍等一下，更自然
                        success = self.sender.send_message(
                            reply,
                            screenshot_dir=f"screenshots/auto_reply/reply_{message_count}"
                        )
                        
                        if success:
                            print(f"  ✅ 已自动回复")
                            
                            # 记录已回复的消息
                            if message_info:
                                msg_content = message_info.get('content', '')
                                msg_hash = hash(msg_content)
                                self.replied_messages.add(msg_hash)
                                self.last_message_content = msg_content
                                print(f"  📌 已记录消息: {msg_hash}")
                            
                            # 发送成功后，更新基准截图，避免把自己的回复当作新消息
                            time.sleep(0.5)  # 等待消息显示
                            self.receiver._has_new_message()  # 重新获取基准，这会更新 last_screenshot
                        else:
                            print(f"  ❌ 回复失败")
                    else:
                        print(f"  ⏭️  跳过回复")
                    
                    print()
        
        except KeyboardInterrupt:
            print("\n\n⏹️  已停止监控")
            print(f"📊 共处理 {message_count} 条消息")

def intelligent_reply_rule(message_info):
    """智能回复规则 - 基于 OCR 识别的内容"""
    if isinstance(message_info, dict):
        msg_type = message_info.get('type', 'unknown')
        content = message_info.get('content', '')
        
        # 语音消息
        if msg_type == 'voice':
            return "收到您的语音，请发送文字消息哦~"
        
        # 图片消息
        if msg_type == 'image':
            return "收到图片"
        
        # 文字消息 - 可以根据内容智能回复
        if msg_type == 'text':
            content_lower = content.lower()
            
            # 简单的关键词回复
            if '你好' in content or 'hello' in content_lower:
                return "你好！有什么可以帮助你的吗？"
            elif '再见' in content or 'bye' in content_lower:
                return "再见！祝你愉快~"
            elif '谢谢' in content or 'thanks' in content_lower:
                return "不客气！"
            elif '?' in content or '？' in content:
                return "收到您的问题，正在思考中..."
            else:
                return f"收到：{content}"
    
    # 降级处理
    return "收到消息"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="微信自动回复系统")
    parser.add_argument("--interval", type=int, default=3, help="检查间隔（秒）")
    parser.add_argument("--mode", choices=["simple", "custom", "intelligent", "rules"], default="rules", 
                       help="回复模式（推荐使用 rules）")
    parser.add_argument("--ocr", action="store_true", help="启用 OCR 识别消息内容")
    parser.add_argument("--ocr-engine", choices=["paddle", "tesseract", "mcp", "docker"], 
                       default="docker", help="OCR 引擎选择（推荐使用 docker）")
    parser.add_argument("--no-rules", action="store_true", help="禁用规则引擎")
    
    args = parser.parse_args()
    
    use_rules = not args.no_rules
    auto_reply = WeChatAutoReply(use_ocr=args.ocr, ocr_engine=args.ocr_engine, use_rules=use_rules)
    
    if args.mode == "rules" or use_rules:
        # 规则模式（默认）
        auto_reply.start_monitoring(check_interval=args.interval)
    elif args.mode == "simple":
        auto_reply.start_monitoring(check_interval=args.interval)
    elif args.mode == "custom":
        auto_reply.start_monitoring(reply_rule=custom_reply_rule, check_interval=args.interval)
    else:  # intelligent
        if not args.ocr:
            print("⚠️  智能模式需要启用 OCR，自动开启...")
            auto_reply.use_ocr = True
            try:
                auto_reply.ocr = MessageOCR(ocr_engine=args.ocr_engine)
            except:
                print("❌ OCR 启动失败，切换到规则模式")
        auto_reply.start_monitoring(reply_rule=intelligent_reply_rule, check_interval=args.interval)
