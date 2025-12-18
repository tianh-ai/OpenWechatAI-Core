#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker Backend OCR 适配器 - 通过 Docker 后端容器调用 PaddleOCR
"""

import subprocess
import os
import json
import tempfile
import shutil

class DockerOCRAdapter:
    """通过 Docker 后端调用 OCR"""
    
    def __init__(self, container_name="bidding_backend"):
        self.container_name = container_name
        self._check_docker()
    
    def _check_docker(self):
        """检查 Docker 是否运行"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={self.container_name}", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if self.container_name not in result.stdout:
                print(f"⚠️  Docker 容器 '{self.container_name}' 未运行")
        except Exception as e:
            print(f"⚠️  无法连接到 Docker: {e}")
    
    def recognize_text(self, image_path):
        """
        识别图片中的文字
        
        Args:
            image_path: 本地图片路径
        
        Returns:
            str: 识别出的文字
        """
        if not os.path.exists(image_path):
            print(f"❌ 图片不存在: {image_path}")
            return ""
        
        # 1. 复制图片到容器内
        container_path = f"/tmp/{os.path.basename(image_path)}"
        
        try:
            subprocess.run(
                ["docker", "cp", image_path, f"{self.container_name}:{container_path}"],
                capture_output=True,
                check=True,
                timeout=10
            )
        except Exception as e:
            print(f"❌ 复制文件到容器失败: {e}")
            return ""
        
        # 2. 在容器中执行 OCR
        python_code = f"""
from paddleocr import PaddleOCR
import json
from PIL import Image

# 初始化OCR，使用更准确的模型
ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False, det_db_thresh=0.3, det_db_box_thresh=0.5)
result = ocr.ocr('{container_path}', cls=True)

# 获取图片宽度（用于判断左右）
img = Image.open('{container_path}')
img_width = img.width

texts = []
text_items = []
if result and result[0]:
    for line in result[0]:
        box = line[0]  # 文字框坐标
        text = line[1][0]
        confidence = line[1][1]
        
        # 提高置信度阈值，只保留高质量识别结果
        if confidence > 0.7:
            # 计算文字框中心x坐标
            center_x = (box[0][0] + box[2][0]) / 2
            # 判断是左侧（对方）还是右侧（自己）
            is_right = center_x > img_width * 0.6  # 右侧60%以上认为是自己发的
            
            text_items.append({{'text': text, 'is_right': is_right, 'center_x': center_x}})

# 只保留左侧（对方）的消息，取最下面的一条
left_texts = [item for item in text_items if not item['is_right']]
if left_texts:
    # 取最后一条
    last_text = left_texts[-1]['text']
    texts = [last_text]
else:
    # 如果没有左侧消息，返回所有文字
    texts = [item['text'] for item in text_items]

print(json.dumps({{'text': '\\n'.join(texts), 'success': True}}))
"""
        
        try:
            # 执行容器命令（降低超时时间）
            result = subprocess.run(
                ["docker", "exec", self.container_name, 
                 "python3", "-c", python_code],
                capture_output=True,
                text=True,
                timeout=15  # 降低到15秒
            )
            
            if result.returncode == 0:
                # 解析 JSON 结果
                try:
                    data = json.loads(result.stdout.strip())
                    return data.get('text', '')
                except json.JSONDecodeError:
                    # 直接返回文本
                    return result.stdout.strip()
            else:
                print(f"❌ OCR 执行失败: {result.stderr}")
                return ""
        
        except subprocess.TimeoutExpired:
            print("❌ OCR 执行超时")
            return ""
        except Exception as e:
            print(f"❌ OCR 错误: {e}")
            return ""
        finally:
            # 清理容器内的临时文件
            try:
                subprocess.run(
                    ["docker", "exec", self.container_name, "rm", "-f", container_path],
                    capture_output=True,
                    timeout=5
                )
            except:
                pass

if __name__ == "__main__":
    import sys
    
    # 测试
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "screenshots/test/received.jpg"
    
    print("="*60)
    print("Docker Backend OCR 测试")
    print("="*60)
    print(f"\n📸 图片: {image_path}")
    
    adapter = DockerOCRAdapter()
    text = adapter.recognize_text(image_path)
    
    print(f"\n📝 识别结果:")
    print("-" * 60)
    print(text if text else "(未识别到文字)")
    print("-" * 60)
