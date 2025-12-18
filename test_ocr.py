#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 OCR 识别之前收到的消息
"""

from message_ocr import MessageOCR
import os

def test_ocr():
    print("="*60)
    print("测试 PaddleOCR 识别微信消息")
    print("="*60)
    
    # 查找测试截图
    test_images = [
        "screenshots/test/received.jpg",
        "screenshots/auto_reply/msg_1.jpg",
        "screenshots/send_with_enter/02_typed.jpg",
    ]
    
    available_images = [img for img in test_images if os.path.exists(img)]
    
    if not available_images:
        print("\n❌ 未找到测试截图")
        print("   请先运行测试生成截图")
        return
    
    try:
        print("\n初始化 PaddleOCR...")
        ocr = MessageOCR(ocr_engine="paddle")
        
        for img_path in available_images:
            print("\n" + "="*60)
            print(f"📸 测试图片: {img_path}")
            print("="*60)
            
            # 识别所有文字
            all_text = ocr.recognize_text(img_path)
            print(f"\n【识别的所有文字】")
            print("-" * 60)
            print(all_text if all_text else "(未识别到文字)")
            print("-" * 60)
            
            # 提取消息
            message = ocr.extract_latest_message(img_path)
            print(f"\n【提取的消息】")
            print(f"  类型: {message['type']}")
            print(f"  内容: {message['content']}")
        
        print("\n" + "="*60)
        print("✅ OCR 测试完成！")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\nPaddleOCR 可能还在安装中...")
        print("安装命令: pip install paddleocr paddlepaddle")

if __name__ == "__main__":
    test_ocr()
