"""
微信平台实现 - 基于uiautomator2的真实UI自动化
"""
import time
import uiautomator2 as u2
from typing import List, Dict, Any, Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from interfaces.message_platform import IMessagePlatform


class WeChatPlatform(IMessagePlatform):
    """微信平台实现"""
    
    # UI元素定位（需要使用weditor实际获取）
    SELECTORS = {
        "chat_list": {"resourceId": "com.tencent.mm:id/e5u"},  # 聊天列表
        "search_btn": {"resourceId": "com.tencent.mm:id/cn1"},  # 搜索按钮
        "search_input": {"resourceId": "com.tencent.mm:id/bhn"},  # 搜索输入框
        "message_input": {"resourceId": "com.tencent.mm:id/aks"},  # 消息输入框
        "send_btn": {"resourceId": "com.tencent.mm:id/akw"},  # 发送按钮
        "message_item": {"resourceId": "com.tencent.mm:id/al_"},  # 消息item
        "red_dot": {"resourceId": "com.tencent.mm:id/e64"},  # 未读红点
        "contact_name": {"resourceId": "com.tencent.mm:id/dyh"},  # 联系人名称
        "latest_message": {"resourceId": "com.tencent.mm:id/e62"},  # 最新消息
    }
    
    def __init__(self, device_serial: str = None):
        """
        初始化微信平台
        
        Args:
            device_serial: 设备序列号（None则使用第一个设备）
        """
        super().__init__()
        
        try:
            self.device = u2.connect(device_serial) if device_serial else u2.connect()
            logger.info(f"连接设备成功: {self.device.info}")
            
            # 检查微信是否安装
            if not self.device.app_info("com.tencent.mm"):
                raise RuntimeError("微信未安装")
            
            # 启动微信
            self._launch_wechat()
            
        except Exception as e:
            logger.error(f"微信平台初始化失败: {e}")
            raise
    
    def _launch_wechat(self):
        """启动微信并返回首页"""
        logger.info("启动微信...")
        self.device.app_start("com.tencent.mm", stop=True)
        time.sleep(3)  # 等待启动
        
        # 确保在聊天列表页
        self.device.press("back")
        self.device.press("back")
        time.sleep(1)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
    def send_message(self, receiver: str, content: str) -> bool:
        """
        发送消息
        
        Args:
            receiver: 接收者（微信昵称或备注名）
            content: 消息内容
            
        Returns:
            是否发送成功
        """
        try:
            logger.info(f"发送消息: {receiver} -> {content[:50]}")
            
            # 1. 返回聊天列表
            self._ensure_chat_list()
            
            # 2. 搜索联系人
            if not self._search_contact(receiver):
                logger.error(f"未找到联系人: {receiver}")
                return False
            
            # 3. 进入聊天窗口
            time.sleep(1)
            
            # 4. 输入消息
            input_box = self.device(**self.SELECTORS["message_input"])
            if not input_box.exists:
                logger.error("未找到消息输入框")
                return False
            
            input_box.click()
            time.sleep(0.5)
            input_box.set_text(content)
            time.sleep(0.5)
            
            # 5. 发送
            send_btn = self.device(**self.SELECTORS["send_btn"])
            if send_btn.exists:
                send_btn.click()
                logger.success(f"消息发送成功: {receiver}")
                return True
            else:
                logger.error("未找到发送按钮")
                return False
                
        except Exception as e:
            logger.error(f"发送消息失败: {e}", exc_info=True)
            return False
    
    def get_unread_messages(self) -> List[Dict[str, Any]]:
        """
        获取未读消息
        
        Returns:
            未读消息列表
        """
        try:
            logger.debug("扫描未读消息...")
            
            # 确保在聊天列表
            self._ensure_chat_list()
            time.sleep(1)
            
            unread_messages = []
            
            # 查找有红点的聊天项
            chat_items = self.device(**self.SELECTORS["chat_list"]).child(
                **self.SELECTORS["message_item"]
            )
            
            for i in range(min(10, chat_items.count)):  # 只检查前10个
                try:
                    # 检查是否有未读标记
                    item = chat_items[i]
                    
                    # 获取联系人名称
                    contact_elem = item.child(**self.SELECTORS["contact_name"])
                    if not contact_elem.exists:
                        continue
                    
                    contact_name = contact_elem.get_text()
                    
                    # 获取最新消息内容
                    message_elem = item.child(**self.SELECTORS["latest_message"])
                    if not message_elem.exists:
                        continue
                    
                    message_content = message_elem.get_text()
                    
                    # 检查是否有红点（未读标记）
                    red_dot = item.child(**self.SELECTORS["red_dot"])
                    if red_dot.exists:
                        # 点击进入聊天
                        item.click()
                        time.sleep(1)
                        
                        # 获取聊天窗口中的消息（可选：更详细的提取）
                        messages = self._extract_chat_messages()
                        
                        # 返回聊天列表
                        self.device.press("back")
                        time.sleep(0.5)
                        
                        # 添加到未读列表
                        for msg in messages:
                            unread_messages.append({
                                "platform": "wechat",
                                "sender": contact_name,
                                "content": msg["content"],
                                "type": msg["type"],
                                "timestamp": time.time()
                            })
                
                except Exception as e:
                    logger.warning(f"处理聊天项失败: {e}")
                    continue
            
            logger.info(f"扫描到 {len(unread_messages)} 条未读消息")
            return unread_messages
            
        except Exception as e:
            logger.error(f"获取未读消息失败: {e}", exc_info=True)
            return []
    
    def _ensure_chat_list(self):
        """确保在聊天列表页面"""
        # 按返回键多次确保退出聊天窗口
        for _ in range(3):
            self.device.press("back")
            time.sleep(0.3)
        
        # 点击"微信"tab（如果不在）
        wechat_tab = self.device(text="微信")
        if wechat_tab.exists:
            wechat_tab.click()
            time.sleep(0.5)
    
    def _search_contact(self, name: str) -> bool:
        """
        搜索联系人并点击
        
        Args:
            name: 联系人名称
            
        Returns:
            是否找到并点击成功
        """
        try:
            # 点击搜索按钮
            search_btn = self.device(**self.SELECTORS["search_btn"])
            if not search_btn.exists:
                logger.error("未找到搜索按钮")
                return False
            
            search_btn.click()
            time.sleep(0.5)
            
            # 输入搜索内容
            search_input = self.device(**self.SELECTORS["search_input"])
            if not search_input.exists:
                logger.error("未找到搜索框")
                return False
            
            search_input.set_text(name)
            time.sleep(1)
            
            # 点击第一个搜索结果
            result = self.device(textContains=name)
            if result.exists:
                result.click()
                return True
            else:
                logger.warning(f"未找到搜索结果: {name}")
                return False
                
        except Exception as e:
            logger.error(f"搜索联系人失败: {e}")
            return False
    
    def _extract_chat_messages(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        从聊天窗口提取最新消息
        
        Args:
            count: 提取数量
            
        Returns:
            消息列表
        """
        messages = []
        
        try:
            # 使用dump_hierarchy获取页面XML
            xml = self.device.dump_hierarchy()
            
            # 简单提取（实际需要更复杂的XML解析）
            # 这里仅作示例
            messages.append({
                "content": "消息内容提取待完善",
                "type": "text"
            })
            
        except Exception as e:
            logger.error(f"提取消息失败: {e}")
        
        return messages
    
    def mark_as_read(self, message_id: str) -> bool:
        """
        标记消息为已读（微信自动标记，无需实现）
        
        Args:
            message_id: 消息ID
            
        Returns:
            是否成功
        """
        return True
    
    def screenshot(self, save_path: str = None) -> str:
        """
        截屏
        
        Args:
            save_path: 保存路径
            
        Returns:
            截图路径
        """
        try:
            if not save_path:
                save_path = f"screenshots/wechat_{int(time.time())}.png"
            
            self.device.screenshot(save_path)
            logger.info(f"截图已保存: {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""
    
    def reconnect(self):
        """重新连接设备"""
        try:
            logger.info("重新连接设备...")
            self.device = u2.connect()
            self._launch_wechat()
            logger.success("重新连接成功")
        except Exception as e:
            logger.error(f"重新连接失败: {e}")
            raise
