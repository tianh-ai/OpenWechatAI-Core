#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP OCR 适配器 - 调用外部 MCP 服务进行 OCR
"""

import asyncio
import os

class MCPOCRAdapter:
    """调用 MCP 服务进行 OCR 的适配器"""
    
    def __init__(self):
        self.server = None
        self._initialized = False
    
    async def _ensure_initialized(self):
        """确保 MCP 服务已初始化"""
        if not self._initialized:
            try:
                # 尝试导入 MCP 服务
                from database_query import DatabaseQueryServer
                self.server = DatabaseQueryServer()
                self._initialized = True
                print("✓ MCP OCR 服务已连接")
            except ImportError:
                raise Exception("无法导入 DatabaseQueryServer，请确认 MCP 服务已安装")
    
    async def ocr_image_async(self, image_path):
        """
        异步 OCR 识别图片
        
        Args:
            image_path: 图片路径
        
        Returns:
            str: 识别出的文字
        """
        await self._ensure_initialized()
        
        # TODO: 调用 MCP 的 OCR 功能
        # 这里需要根据你的 MCP 实际 API 来调整
        
        # 假设 MCP 有 OCR 功能接口
        # result = await self.server.ocr_recognize(image_path)
        # return result['text']
        
        # 临时方案：如果 MCP 中集成了 PaddleOCR，直接调用
        try:
            from paddleocr import PaddleOCR
            ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
            result = ocr.ocr(image_path, cls=True)
            
            if not result or not result[0]:
                return ""
            
            texts = []
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                if confidence > 0.5:
                    texts.append(text)
            
            return "\n".join(texts)
        except Exception as e:
            raise Exception(f"OCR 识别失败: {e}")
    
    def ocr_image(self, image_path):
        """
        同步 OCR 识别图片（包装异步方法）
        
        Args:
            image_path: 图片路径
        
        Returns:
            str: 识别出的文字
        """
        return asyncio.run(self.ocr_image_async(image_path))
    
    async def cleanup(self):
        """清理资源"""
        if self.server and hasattr(self.server, 'cleanup'):
            await self.server.cleanup()

if __name__ == "__main__":
    async def test():
        adapter = MCPOCRAdapter()
        
        # 测试 OCR
        test_image = "screenshots/test/received.jpg"
        if os.path.exists(test_image):
            print(f"测试图片: {test_image}")
            text = await adapter.ocr_image_async(test_image)
            print(f"识别结果:\n{text}")
        else:
            print(f"测试图片不存在: {test_image}")
        
        await adapter.cleanup()
    
    asyncio.run(test())
