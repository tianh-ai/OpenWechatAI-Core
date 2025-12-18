#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR 消息识别模块 - 支持 PaddleOCR
"""

import os
from PIL import Image

class MessageOCR:
    def __init__(self, ocr_engine="paddle"):
        """
        初始化 OCR 引擎
        
        Args:
            ocr_engine: "paddle" 或 "tesseract" 或 "mcp" 或 "docker"
        """
        self.engine = ocr_engine
        self.ocr = None
        
        if ocr_engine == "paddle":
            self._init_paddle()
        elif ocr_engine == "tesseract":
            self._init_tesseract()
        elif ocr_engine == "mcp":
            self._init_mcp()
        elif ocr_engine == "docker":
            self._init_docker()
    
    def _init_paddle(self):
        """初始化 PaddleOCR"""
        try:
            from paddleocr import PaddleOCR
            # use_angle_cls=True 识别旋转文字
            # lang='ch' 中文+英文
            self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
            print("✓ PaddleOCR 初始化成功")
        except ImportError:
            print("❌ PaddleOCR 未安装，请运行: pip install paddleocr")
            raise
    
    def _init_tesseract(self):
        """初始化 Tesseract"""
        try:
            import pytesseract
            self.ocr = pytesseract
            print("✓ Tesseract 初始化成功")
        except ImportError:
            print("❌ pytesseract 未安装，请运行: pip install pytesseract")
            raise
    
    def _init_mcp(self):
        """初始化 MCP OCR"""
        try:
            from mcp_ocr_adapter import MCPOCRAdapter
            self.ocr = MCPOCRAdapter()
            print("✓ MCP OCR 初始化成功")
        except Exception as e:
            print(f"❌ MCP OCR 初始化失败: {e}")
            print("   将尝试使用 PaddleOCR 作为后备")
            self._init_paddle()
    
    def _init_docker(self):
        """初始化 Docker Backend OCR"""
        try:
            from docker_ocr_adapter import DockerOCRAdapter
            self.ocr = DockerOCRAdapter()
            print("✓ Docker Backend OCR 初始化成功")
        except Exception as e:
            print(f"❌ Docker OCR 初始化失败: {e}")
            raise
    
    def recognize_text(self, image_path):
        """
        识别图片中的文字
        
        Args:
            image_path: 图片路径
        
        Returns:
            str: 识别出的文字内容
        """
        if not os.path.exists(image_path):
            print(f"❌ 图片不存在: {image_path}")
            return ""
        
        if self.engine == "paddle":
            return self._recognize_with_paddle(image_path)
        elif self.engine == "tesseract":
            return self._recognize_with_tesseract(image_path)
        elif self.engine == "mcp":
            return self._recognize_with_mcp(image_path)
        elif self.engine == "docker":
            return self._recognize_with_docker(image_path)
        
        return ""
    
    def _recognize_with_paddle(self, image_path):
        """使用 PaddleOCR 识别"""
        result = self.ocr.ocr(image_path, cls=True)
        
        if not result or not result[0]:
            return ""
        
        # 提取所有文字，按位置从上到下排序
        texts = []
        for line in result[0]:
            text = line[1][0]  # 文字内容
            confidence = line[1][1]  # 置信度
            
            # 只保留置信度高于 0.5 的结果
            if confidence > 0.5:
                texts.append(text)
        
        return "\n".join(texts)
    
    def _recognize_with_tesseract(self, image_path):
        """使用 Tesseract 识别"""
        img = Image.open(image_path)
        # lang='chi_sim+eng' 中文简体+英文
        text = self.ocr.image_to_string(img, lang='chi_sim+eng')
        return text.strip()
    
    def _recognize_with_mcp(self, image_path):
        """使用 MCP OCR 识别"""
        try:
            # MCP 适配器的同步调用
            text = self.ocr.ocr_image(image_path)
            return text.strip()
        except Exception as e:
            print(f"❌ MCP OCR 识别失败: {e}")
            return ""
    
    def _recognize_with_docker(self, image_path):
        """使用 Docker Backend OCR 识别"""
        try:
            text = self.ocr.recognize_text(image_path)
            return text.strip()
        except Exception as e:
            print(f"❌ Docker OCR 识别失败: {e}")
            return ""
    
    def extract_latest_message(self, chat_screenshot):
        """
        从聊天截图中提取最新消息
        
        Args:
            chat_screenshot: 聊天区域截图路径
        
        Returns:
            dict: {"type": "text/voice/image", "sender": "...", "content": "...", "is_self": bool}
        """
        # 识别所有文字
        all_text = self.recognize_text(chat_screenshot)
        
        if not all_text:
            return {
                "type": "unknown", 
                "sender": "", 
                "content": "",
                "is_self": False
            }
        
        # 提取发送者（通常在消息上方）
        sender = "未知"
        lines = all_text.strip().split('\n')
        
        # 过滤掉自己的回复消息（识别特征：包含之前发送的回复内容）
        # 获取最后一条非自己的消息
        message_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 过滤掉明显是自己发送的消息
            if "收到" in line and ("自动回复" in line or "您的消息" in line):
                continue
            message_lines.append(line)
        
        if not message_lines:
            return {
                "type": "unknown",
                "sender": "",
                "content": "",
                "is_self": False
            }
        
        # 检查是否是自己发送的消息（简化处理）
        is_self = False
        
        # 第一行通常是发送者或联系人名称
        if message_lines:
            sender = message_lines[0] if message_lines[0] else "未知"
        
        # 检查是否是语音消息
        if "[语音]" in all_text or "\"" in all_text:
            content = message_lines[-1] if message_lines else all_text
            return {
                "type": "voice", 
                "sender": sender,
                "content": content,
                "is_self": is_self
            }
        
        # 检查是否是图片消息
        if "[图片]" in all_text:
            content = message_lines[-1] if message_lines else all_text
            return {
                "type": "image", 
                "sender": sender,
                "content": content,
                "is_self": is_self
            }
        
        # 获取最后一条消息（最新的）
        if message_lines:
            # 最后一行通常是最新消息内容
            latest = message_lines[-1]
            return {
                "type": "text", 
                "sender": sender,
                "content": latest,
                "is_self": is_self
            }
        
        return {
            "type": "unknown", 
            "sender": "",
            "content": "",
            "is_self": False
        }
    
    def _is_system_message(self, text):
        """判断是否是系统消息"""
        # 时间格式：上午、下午、昨天等
        system_keywords = [
            "上午", "下午", "昨天", "今天", 
            ":", "：",  # 时间分隔符
            "文件传输助手",  # 联系人名称
        ]
        
        # 如果只包含这些关键词，可能是系统消息
        if len(text) < 15:  # 短文本
            for keyword in system_keywords:
                if keyword in text:
                    return True
        
        return False

if __name__ == "__main__":
    import sys
    
    # 测试 OCR
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # 使用测试截图
        image_path = "screenshots/test/received.jpg"
    
    print("="*60)
    print("OCR 消息识别测试")
    print("="*60)
    
    try:
        ocr = MessageOCR(ocr_engine="paddle")
        
        print(f"\n📸 图片: {image_path}")
        
        # 识别所有文字
        all_text = ocr.recognize_text(image_path)
        print(f"\n📝 识别的所有文字:")
        print("-" * 60)
        print(all_text)
        print("-" * 60)
        
        # 提取最新消息
        message = ocr.extract_latest_message(image_path)
        print(f"\n💬 提取的最新消息:")
        print(f"   类型: {message['type']}")
        print(f"   内容: {message['content']}")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n如果 PaddleOCR 未安装，请运行:")
        print("  pip install paddleocr paddlepaddle")
