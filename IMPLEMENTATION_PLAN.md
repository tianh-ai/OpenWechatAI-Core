# OpenWechatAI-Core 实施规划
> 基于现有代码库的完整实施路线图  
> 更新日期: 2025-12-16

## 📋 目录
- [当前状态评估](#当前状态评估)
- [整体优化方案](#整体优化方案)
- [详细实施步骤](#详细实施步骤)
- [技术栈升级](#技术栈升级)
- [架构改进](#架构改进)
- [生产部署方案](#生产部署方案)

---

## 🔍 当前状态评估

### ✅ 已完成的部分
1. **基础架构框架**
   - ✓ 五层架构设计（规则、逻辑、技能、接口、实现）
   - ✓ 接口层：`IMessagePlatform` 抽象基类
   - ✓ 实现层：`WeChatPlatform` 基础实现
   - ✓ 技能层：`BaseSkill` 和 `EchoSkill` 示例
   - ✓ 异步任务：Celery + Redis 集成
   - ✓ 消息监听：`run_wechat_listener` 轮询机制

2. **依赖管理**
   - ✓ requirements.txt 包含核心依赖
   - ✓ 配置管理：Pydantic Settings

### ⚠️ 需要完善的部分
1. **核心功能缺失**
   - ❌ 微信UI自动化实现（仅有伪代码）
   - ❌ AI集成（OpenAI/Gemini）
   - ❌ 规则引擎（YAML解析器）
   - ❌ 插件管理系统
   - ❌ 数据库模型和ORM

2. **工程化不足**
   - ❌ 日志系统未配置
   - ❌ 异常处理不完善
   - ❌ 单元测试缺失
   - ❌ 监控和告警
   - ❌ 容器化配置

3. **安全性**
   - ❌ 敏感信息加密
   - ❌ API认证授权
   - ❌ 速率限制

---

## 🚀 整体优化方案

### 1. 架构升级（保持五层核心，增强扩展性）

```
┌─────────────────────────────────────────────────────────────┐
│                      前端层 (Frontend)                       │
│          Web管理界面 (FastAPI + Vue/React)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     规则层 (Rules)                           │
│    规则引擎 + YAML配置 + 动态热加载                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    逻辑层 (Logic)                            │
│  事件调度器 + AI决策引擎 + 插件管理器 + 上下文管理           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    技能层 (Skills)                           │
│  插件化技能 + 技能注册表 + 技能优先级 + 技能链               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   接口层 (Interfaces)                        │
│  IMessagePlatform + IControlBridge + IAIModel + IDatabase    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   实现层 (Implementations)                   │
│  微信 + 飞书 + 钉钉 + OpenAI + Gemini + PostgreSQL           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 基础设施层 (Infrastructure)                  │
│  日志 + 监控 + 缓存 + 消息队列 + 数据库 + 对象存储            │
└─────────────────────────────────────────────────────────────┘
```

### 2. 新增核心组件

#### 2.1 事件驱动架构
```python
# 事件总线
EventBus → Event Handlers → Async Tasks
```

#### 2.2 插件系统
```python
# 动态插件加载
PluginManager → PluginRegistry → PluginExecutor
```

#### 2.3 AI决策引擎
```python
# 多模型支持
AIOrchestrator → [OpenAI, Gemini, Claude] → Response
```

#### 2.4 监控体系
```python
# 全链路监控
Prometheus + Grafana + Sentry + Custom Metrics
```

---

## 📝 详细实施步骤

### 阶段一：基础设施完善（优先级：🔴 高）

#### Step 1.1: 完善配置管理
**目标**: 统一配置，支持多环境

**任务**:
- [ ] 创建 `.env.example` 模板
- [ ] 扩展 `core/config.py` 支持多环境配置
- [ ] 添加配置验证
- [ ] 实现敏感信息加密（使用 `cryptography`）

**文件**:
```python
# core/config.py (优化版)
from pydantic_settings import BaseSettings
from typing import Optional
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # 环境
    environment: Environment = Environment.DEVELOPMENT
    debug: bool = False
    
    # 数据库
    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20
    
    # Redis
    redis_url: str
    redis_max_connections: int = 50
    
    # 消息队列
    celery_broker_url: str
    celery_result_backend: str
    
    # AI APIs
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    gemini_api_key: Optional[str] = None
    
    # 平台集成
    feishu_app_id: Optional[str] = None
    feishu_app_secret: Optional[str] = None
    
    # 安全
    secret_key: str
    allowed_hosts: list[str] = ["*"]
    
    # 日志
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # 监控
    sentry_dsn: Optional[str] = None
    enable_metrics: bool = True
    
    # 手机控制
    android_device_serial: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

#### Step 1.2: 建立日志系统
**目标**: 统一日志管理，结构化日志

**任务**:
- [ ] 配置 `loguru` 日志
- [ ] 实现日志分级（DEBUG/INFO/WARNING/ERROR）
- [ ] 日志轮转和归档
- [ ] 集成 Sentry 错误追踪

**文件**:
```python
# core/logging.py
from loguru import logger
import sys
from core.config import settings

def setup_logging():
    """配置应用日志"""
    # 移除默认handler
    logger.remove()
    
    # 控制台输出
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True
    )
    
    # 文件输出
    logger.add(
        settings.log_file,
        rotation="500 MB",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        enqueue=True  # 异步写入
    )
    
    # 错误单独记录
    logger.add(
        "logs/errors.log",
        rotation="100 MB",
        retention="60 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
        backtrace=True,
        diagnose=True
    )
    
    return logger
```

#### Step 1.3: 数据库模型设计
**目标**: 持久化消息、用户、规则等数据

**任务**:
- [ ] 设计数据库Schema
- [ ] 创建 SQLAlchemy 模型
- [ ] 实现数据库迁移（Alembic）
- [ ] 添加数据库连接池

**文件**:
```python
# models/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,  # 连接健康检查
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """依赖注入：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
# models/message.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from models.database import Base

class MessageStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, index=True)
    sender = Column(String(255), nullable=False, index=True)
    receiver = Column(String(255))
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text")  # text, image, voice
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime)
    
    # 关联响应
    responses = relationship("MessageResponse", back_populates="message")

class MessageResponse(Base):
    __tablename__ = "message_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    skill_name = Column(String(100))
    response_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    message = relationship("Message", back_populates="responses")
```

---

### 阶段二：核心功能实现（优先级：🔴 高）

#### Step 2.1: 完善微信UI自动化
**目标**: 实现真实的微信控制逻辑

**任务**:
- [ ] UI元素定位策略（resourceId, text, xpath）
- [ ] 实现发送消息功能
- [ ] 实现获取未读消息
- [ ] 实现联系人管理
- [ ] 添加截图和OCR支持
- [ ] 异常重试机制

**关键代码**:
```python
# implementations/wechat/wechat_platform.py (完整实现)
import uiautomator2 as u2
from typing import List, Dict, Any, Optional
from interfaces.message_platform import IMessagePlatform
from tenacity import retry, stop_after_attempt, wait_exponential
from core.logging import logger
import time

class WeChatPlatform(IMessagePlatform):
    """微信平台完整实现"""
    
    # UI元素定位器
    LOCATORS = {
        "search_button": {"text": "搜索"},
        "message_input": {"resourceId": "com.tencent.mm:id/aln"},
        "send_button": {"text": "发送"},
        "chat_list": {"resourceId": "com.tencent.mm:id/e6e"},
        "unread_badge": {"resourceId": "com.tencent.mm:id/ov"},
    }
    
    def __init__(self, device_serial: Optional[str] = None):
        self.device_serial = device_serial
        self.d: Optional[u2.Device] = None
        self._platform_name = "WeChat"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def connect(self) -> bool:
        """连接设备并启动微信"""
        try:
            self.d = u2.connect(self.device_serial)
            logger.info(f"已连接设备: {self.d.device_info.get('serial')}")
            
            # 启动微信
            self.d.app_start("com.tencent.mm", stop=True)
            time.sleep(3)  # 等待启动
            
            # 验证是否在微信主界面
            if self.d(text="微信").exists(timeout=10):
                logger.success("微信启动成功")
                return True
            
            logger.error("未能进入微信主界面")
            return False
            
        except Exception as e:
            logger.error(f"连接失败: {e}")
            raise
    
    def disconnect(self) -> None:
        """断开连接"""
        if self.d:
            self.d.app_stop("com.tencent.mm")
            logger.info("已停止微信")
    
    def send_message(self, contact_id: str, message: str) -> bool:
        """发送消息的完整实现"""
        try:
            # 1. 返回主界面
            self._go_to_main()
            
            # 2. 搜索联系人
            if not self._search_contact(contact_id):
                logger.error(f"未找到联系人: {contact_id}")
                return False
            
            # 3. 进入聊天界面
            self.d(text=contact_id).click()
            time.sleep(1)
            
            # 4. 输入消息
            input_box = self.d(**self.LOCATORS["message_input"])
            if not input_box.exists(timeout=5):
                logger.error("未找到输入框")
                return False
            
            input_box.click()
            input_box.set_text(message)
            time.sleep(0.5)
            
            # 5. 发送
            send_btn = self.d(**self.LOCATORS["send_button"])
            if send_btn.exists(timeout=3):
                send_btn.click()
                logger.success(f"已发送消息给 {contact_id}: {message[:50]}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False
    
    def get_unread_messages(self) -> List[Dict[str, Any]]:
        """获取未读消息"""
        messages = []
        try:
            self._go_to_main()
            
            # 获取聊天列表
            chat_list = self.d(**self.LOCATORS["chat_list"])
            if not chat_list.exists(timeout=5):
                return messages
            
            # 遍历聊天项
            for i in range(chat_list.child_count):
                chat_item = chat_list.child(instance=i)
                
                # 检查是否有未读标记
                if chat_item.child(**self.LOCATORS["unread_badge"]).exists:
                    sender = self._extract_sender(chat_item)
                    preview = self._extract_preview(chat_item)
                    
                    messages.append({
                        "sender": sender,
                        "content": preview,
                        "platform": self.platform_name,
                        "timestamp": datetime.now().isoformat()
                    })
            
            logger.info(f"发现 {len(messages)} 条未读消息")
            return messages
            
        except Exception as e:
            logger.error(f"获取未读消息失败: {e}")
            return messages
    
    # 辅助方法
    def _go_to_main(self):
        """返回微信主界面"""
        for _ in range(3):
            self.d.press("back")
            time.sleep(0.5)
            if self.d(text="微信").exists:
                break
    
    def _search_contact(self, contact_name: str) -> bool:
        """搜索联系人"""
        search_btn = self.d(**self.LOCATORS["search_button"])
        if search_btn.exists(timeout=5):
            search_btn.click()
            time.sleep(0.5)
            self.d.send_keys(contact_name, clear=True)
            time.sleep(1)
            return self.d(text=contact_name).exists(timeout=5)
        return False
    
    # ... 其他辅助方法
```

#### Step 2.2: AI集成
**目标**: 集成多种AI模型

**任务**:
- [ ] 创建AI接口抽象
- [ ] 实现OpenAI集成
- [ ] 实现Gemini集成
- [ ] AI模型路由器
- [ ] 上下文管理
- [ ] Token计数和成本追踪

**文件**:
```python
# interfaces/ai_model.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class AIMessage:
    """AI消息封装"""
    def __init__(self, role: str, content: str):
        self.role = role  # system, user, assistant
        self.content = content

class IAIModel(ABC):
    """AI模型接口"""
    
    @abstractmethod
    async def chat(
        self, 
        messages: List[AIMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """聊天补全"""
        pass
    
    @abstractmethod
    async def stream_chat(
        self,
        messages: List[AIMessage],
        temperature: float = 0.7
    ):
        """流式聊天"""
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
```

```python
# implementations/ai/openai_model.py
from openai import AsyncOpenAI
from interfaces.ai_model import IAIModel, AIMessage
from typing import List
from core.config import settings
from core.logging import logger

class OpenAIModel(IAIModel):
    """OpenAI GPT 实现"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo-preview"):
        self.client = AsyncOpenAI(api_key=api_key or settings.openai_api_key)
        self._model_name = model
    
    async def chat(
        self, 
        messages: List[AIMessage],
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self._model_name,
                messages=[{"role": msg.role, "content": msg.content} for msg in messages],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            
            # 记录使用情况
            logger.info(f"OpenAI 使用: {response.usage.total_tokens} tokens")
            
            return content
            
        except Exception as e:
            logger.error(f"OpenAI 调用失败: {e}")
            raise
    
    async def stream_chat(self, messages: List[AIMessage], temperature: float = 0.7):
        try:
            stream = await self.client.chat.completions.create(
                model=self._model_name,
                messages=[{"role": msg.role, "content": msg.content} for msg in messages],
                temperature=temperature,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"OpenAI 流式调用失败: {e}")
            raise
    
    @property
    def model_name(self) -> str:
        return self._model_name
```

#### Step 2.3: 规则引擎实现
**目标**: 解析和执行YAML规则

**任务**:
- [ ] 规则YAML Schema设计
- [ ] 规则解析器
- [ ] 规则匹配引擎
- [ ] 规则热加载
- [ ] 规则优先级

**文件**:
```python
# core/rules_engine.py
import yaml
from typing import List, Dict, Any, Callable
from pathlib import Path
from core.logging import logger
import re

class Rule:
    """规则对象"""
    def __init__(self, config: Dict[str, Any]):
        self.name = config.get("name", "unnamed_rule")
        self.conditions = config.get("if", {})
        self.actions = config.get("then", {})
        self.priority = config.get("priority", 0)
        self.enabled = config.get("enabled", True)
    
    def matches(self, message: Dict[str, Any]) -> bool:
        """检查消息是否匹配规则"""
        if not self.enabled:
            return False
        
        # 平台匹配
        if "platform" in self.conditions:
            if message.get("platform") != self.conditions["platform"]:
                return False
        
        # 发送者匹配
        if "sender" in self.conditions:
            pattern = self.conditions["sender"]
            if not re.match(pattern, message.get("sender", "")):
                return False
        
        # 内容匹配
        if "content_contains" in self.conditions:
            keyword = self.conditions["content_contains"]
            if keyword not in message.get("content", ""):
                return False
        
        if "content_regex" in self.conditions:
            pattern = self.conditions["content_regex"]
            if not re.search(pattern, message.get("content", "")):
                return False
        
        return True

class RulesEngine:
    """规则引擎"""
    
    def __init__(self, rules_dir: str = "rules"):
        self.rules_dir = Path(rules_dir)
        self.rules: List[Rule] = []
        self.load_rules()
    
    def load_rules(self):
        """加载所有规则文件"""
        self.rules.clear()
        
        for rule_file in self.rules_dir.glob("*.yaml"):
            try:
                with open(rule_file, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    
                if isinstance(config, list):
                    for rule_config in config:
                        self.rules.append(Rule(rule_config))
                else:
                    self.rules.append(Rule(config))
                
                logger.info(f"已加载规则文件: {rule_file.name}")
                
            except Exception as e:
                logger.error(f"加载规则文件失败 {rule_file}: {e}")
        
        # 按优先级排序
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        logger.success(f"共加载 {len(self.rules)} 条规则")
    
    def find_matching_rules(self, message: Dict[str, Any]) -> List[Rule]:
        """查找匹配的规则"""
        return [rule for rule in self.rules if rule.matches(message)]
    
    def reload(self):
        """热加载规则"""
        logger.info("重新加载规则...")
        self.load_rules()
```

**规则文件示例**:
```yaml
# rules/auto_reply.yaml
- name: "老板紧急消息转发"
  priority: 100
  enabled: true
  if:
    platform: "WeChat"
    sender: "老板"
    content_contains: "紧急"
  then:
    action: "forward"
    target: "DingTalk"
    notify_channels: ["email", "sms"]
    message_template: "⚠️ 紧急消息来自微信老板: {content}"

- name: "自动回复关键词"
  priority: 50
  enabled: true
  if:
    platform: "WeChat"
    content_regex: "^(价格|报价|多少钱)"
  then:
    action: "auto_reply"
    skill: "PriceQuerySkill"
    use_ai: true
    ai_model: "gpt-4"

- name: "工作时间外自动回复"
  priority: 30
  enabled: true
  if:
    platform: "WeChat"
    time_range: "18:00-09:00"
  then:
    action: "auto_reply"
    message: "您好，我现在不在工作时间，明天会尽快回复您。"
```

---

### 阶段三：插件系统（优先级：🟡 中）

#### Step 3.1: 插件管理器
**目标**: 动态加载和管理技能插件

**任务**:
- [ ] 插件发现机制
- [ ] 插件注册表
- [ ] 插件生命周期管理
- [ ] 插件依赖管理
- [ ] 插件隔离

**文件**:
```python
# core/plugin_manager.py
from typing import Dict, List, Type, Optional
from pathlib import Path
import importlib
import inspect
from skills.base_skill import BaseSkill
from core.logging import logger

class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugins_dir: str = "skills"):
        self.plugins_dir = Path(plugins_dir)
        self.registry: Dict[str, Type[BaseSkill]] = {}
        self.instances: Dict[str, BaseSkill] = {}
    
    def discover_plugins(self):
        """自动发现插件"""
        logger.info("开始扫描插件...")
        
        for plugin_file in self.plugins_dir.glob("*_skill.py"):
            if plugin_file.name.startswith("_"):
                continue
            
            try:
                # 动态导入模块
                module_name = f"skills.{plugin_file.stem}"
                module = importlib.import_module(module_name)
                
                # 查找BaseSkill的子类
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseSkill) and obj != BaseSkill:
                        self.register_plugin(name, obj)
                        
            except Exception as e:
                logger.error(f"加载插件失败 {plugin_file}: {e}")
        
        logger.success(f"发现 {len(self.registry)} 个插件")
    
    def register_plugin(self, name: str, plugin_class: Type[BaseSkill]):
        """注册插件"""
        if name in self.registry:
            logger.warning(f"插件 {name} 已存在，将被覆盖")
        
        self.registry[name] = plugin_class
        logger.info(f"已注册插件: {name}")
    
    def get_plugin(self, name: str) -> Optional[BaseSkill]:
        """获取插件实例（单例）"""
        if name not in self.instances:
            if name not in self.registry:
                logger.error(f"未找到插件: {name}")
                return None
            
            # 实例化
            self.instances[name] = self.registry[name]()
        
        return self.instances[name]
    
    def find_handler(self, message: Dict[str, Any]) -> Optional[BaseSkill]:
        """查找能处理消息的插件"""
        for instance in self.instances.values():
            if instance.can_handle(message):
                return instance
        
        # 尝试实例化未加载的插件
        for name, plugin_class in self.registry.items():
            if name not in self.instances:
                instance = plugin_class()
                self.instances[name] = instance
                if instance.can_handle(message):
                    return instance
        
        return None
```

#### Step 3.2: 增强技能系统
**新增高级技能**:
- [ ] AI对话技能
- [ ] 图片识别技能
- [ ] 语音转文字技能
- [ ] 定时任务技能
- [ ] 数据库查询技能
- [ ] 第三方API调用技能

**示例**:
```python
# skills/ai_chat_skill.py
from typing import Dict, Any
from skills.base_skill import BaseSkill
from interfaces.message_platform import IMessagePlatform
from core.logging import logger
from implementations.ai.openai_model import OpenAIModel
from interfaces.ai_model import AIMessage

class AIChatSkill(BaseSkill):
    """AI智能对话技能"""
    
    def __init__(self):
        self.ai_model = OpenAIModel()
        self.context_store = {}  # 简单的上下文存储
    
    @property
    def name(self) -> str:
        return "AI Chat Skill"
    
    def can_handle(self, message: Dict[str, Any]) -> bool:
        """当消息以@AI开头时触发"""
        content = message.get("content", "")
        return content.startswith("@AI") or content.startswith("@ai")
    
    async def execute(self, message: Dict[str, Any], platform: IMessagePlatform) -> None:
        """执行AI对话"""
        sender = message.get("sender")
        content = message.get("content", "").replace("@AI", "").replace("@ai", "").strip()
        
        logger.info(f"AI对话请求来自 {sender}: {content}")
        
        try:
            # 获取历史上下文
            context = self.context_store.get(sender, [])
            context.append(AIMessage("user", content))
            
            # 调用AI
            response = await self.ai_model.chat(context, temperature=0.8)
            
            # 更新上下文
            context.append(AIMessage("assistant", response))
            self.context_store[sender] = context[-10:]  # 保留最近10轮对话
            
            # 发送响应
            platform.send_message(sender, response)
            logger.success(f"AI回复已发送给 {sender}")
            
        except Exception as e:
            logger.error(f"AI对话失败: {e}")
            platform.send_message(sender, "抱歉，AI服务暂时不可用。")
```

---

### 阶段四：Web管理界面（优先级：🟡 中）

#### Step 4.1: FastAPI后端
**目标**: 提供RESTful API

**任务**:
- [ ] API路由设计
- [ ] 认证授权（JWT）
- [ ] 消息历史查询
- [ ] 规则管理API
- [ ] 插件管理API
- [ ] 实时监控API

**文件**:
```python
# api/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.database import get_db
from core.config import settings
from core.logging import logger

app = FastAPI(
    title="OpenWechatAI API",
    description="智能微信机器人管理平台",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
from api.routers import messages, rules, plugins, monitoring

app.include_router(messages.router, prefix="/api/v1/messages", tags=["消息"])
app.include_router(rules.router, prefix="/api/v1/rules", tags=["规则"])
app.include_router(plugins.router, prefix="/api/v1/plugins", tags=["插件"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["监控"])

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "version": "2.0.0"}
```

```python
# api/routers/messages.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db
from models.message import Message
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/", response_model=List[MessageSchema])
async def get_messages(
    skip: int = 0,
    limit: int = 100,
    platform: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取消息列表"""
    query = db.query(Message)
    
    if platform:
        query = query.filter(Message.platform == platform)
    
    if start_date:
        query = query.filter(Message.created_at >= start_date)
    
    if end_date:
        query = query.filter(Message.created_at <= end_date)
    
    messages = query.offset(skip).limit(limit).all()
    return messages

@router.get("/stats")
async def get_message_stats(db: Session = Depends(get_db)):
    """消息统计"""
    total = db.query(Message).count()
    today = db.query(Message).filter(
        Message.created_at >= datetime.now().date()
    ).count()
    
    return {
        "total": total,
        "today": today,
        "platforms": db.query(Message.platform, func.count(Message.id))
                      .group_by(Message.platform).all()
    }
```

---

### 阶段五：生产部署（优先级：🟢 低，但重要）

#### Step 5.1: Docker化
**任务**:
- [ ] 编写Dockerfile
- [ ] docker-compose配置
- [ ] 多阶段构建优化
- [ ] 健康检查

**文件**:
```dockerfile
# Dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 最终镜像
FROM python:3.11-slim

WORKDIR /app

# 复制依赖
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# 启动命令
CMD ["python", "-m", "core.main", "listener"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: openwechatai
      POSTGRES_USER: wechat
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U wechat"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  app:
    build: .
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://wechat:${DB_PASSWORD}@postgres:5432/openwechatai
      REDIS_URL: redis://redis:6379/0
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - ./logs:/app/logs
      - ./rules:/app/rules
    restart: unless-stopped

  celery-worker:
    build: .
    command: celery -A core.tasks worker --loglevel=info
    depends_on:
      - redis
      - postgres
    environment:
      DATABASE_URL: postgresql://wechat:${DB_PASSWORD}@postgres:5432/openwechatai
      REDIS_URL: redis://redis:6379/0
    restart: unless-stopped

  api:
    build: .
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://wechat:${DB_PASSWORD}@postgres:5432/openwechatai
      REDIS_URL: redis://redis:6379/0
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

#### Step 5.2: CI/CD Pipeline
**任务**:
- [ ] GitHub Actions配置
- [ ] 自动测试
- [ ] 自动构建
- [ ] 自动部署

**文件**:
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t openwechatai:latest .
    
    - name: Push to registry
      run: |
        echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
        docker tag openwechatai:latest ${{ secrets.DOCKER_REGISTRY }}/openwechatai:latest
        docker push ${{ secrets.DOCKER_REGISTRY }}/openwechatai:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_SSH_KEY }}
        script: |
          cd /opt/openwechatai
          docker-compose pull
          docker-compose up -d
```

---

## 🔧 技术栈升级建议

### 新增依赖
```txt
# requirements.txt (完整版)

# 核心框架
uiautomator2==2.16.23
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic[dotenv]==2.5.0
pydantic-settings==2.1.0

# 异步任务
celery==5.3.4
redis==5.0.1

# 数据库
SQLAlchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
asyncpg==0.29.0

# 日志和监控
loguru==0.7.2
sentry-sdk==1.38.0
prometheus-client==0.19.0

# AI集成
openai==1.3.7
google-generativeai==0.3.1
anthropic==0.7.5

# 重试和容错
tenacity==8.2.3

# 配置和环境
python-dotenv==1.0.0
pyyaml==6.0.1

# HTTP客户端
httpx==0.25.2
aiohttp==3.9.1

# 图像处理
Pillow==10.1.0
pytesseract==0.3.10  # OCR

# 测试
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
faker==20.1.0

# 安全
cryptography==41.0.7
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# 工具
python-multipart==0.0.6
email-validator==2.1.0
```

---

## 📊 监控和告警

### Prometheus指标
```python
# core/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# 消息计数器
message_counter = Counter(
    'messages_total',
    'Total number of messages processed',
    ['platform', 'status']
)

# 处理时间
processing_time = Histogram(
    'message_processing_seconds',
    'Time spent processing messages',
    ['skill']
)

# 活跃连接数
active_connections = Gauge(
    'active_platform_connections',
    'Number of active platform connections',
    ['platform']
)

# AI调用统计
ai_calls = Counter(
    'ai_api_calls_total',
    'Total AI API calls',
    ['model', 'status']
)
```

---

## 🎯 优先级矩阵

| 阶段 | 任务 | 优先级 | 预计时间 | 依赖 |
|------|------|--------|----------|------|
| 1.1 | 配置管理 | 🔴 高 | 2天 | 无 |
| 1.2 | 日志系统 | 🔴 高 | 1天 | 1.1 |
| 1.3 | 数据库模型 | 🔴 高 | 3天 | 1.1 |
| 2.1 | 微信UI自动化 | 🔴 高 | 5天 | 1.2 |
| 2.2 | AI集成 | 🔴 高 | 3天 | 1.1 |
| 2.3 | 规则引擎 | 🔴 高 | 4天 | 1.3 |
| 3.1 | 插件管理器 | 🟡 中 | 2天 | 2.3 |
| 3.2 | 高级技能 | 🟡 中 | 5天 | 2.2, 3.1 |
| 4.1 | FastAPI后端 | 🟡 中 | 4天 | 1.3 |
| 5.1 | Docker化 | 🟢 低 | 2天 | 全部 |
| 5.2 | CI/CD | 🟢 低 | 2天 | 5.1 |

**总预计时间**: 约 33 天（单人开发）

---

## 🚦 下一步行动

### 立即开始（本周）
1. ✅ 创建 `.env.example` 和完善 `config.py`
2. ✅ 设置 `loguru` 日志系统
3. ✅ 设计并创建数据库模型
4. ✅ 运行数据库迁移

### 短期目标（2周内）
1. 完成微信UI自动化核心功能
2. 集成OpenAI API
3. 实现基础规则引擎
4. 编写3-5个实用技能插件

### 中期目标（1个月内）
1. 完善插件系统
2. 开发Web管理界面
3. 添加监控和告警
4. 完成单元测试（覆盖率>80%）

### 长期目标（2-3个月）
1. 生产环境部署
2. 性能优化
3. 支持更多平台（飞书、钉钉）
4. 高级AI功能（多模态、RAG）

---

## 📚 参考资源

- **uiautomator2文档**: https://github.com/openatx/uiautomator2
- **FastAPI文档**: https://fastapi.tiangolo.com/
- **Celery最佳实践**: https://docs.celeryq.dev/
- **SQLAlchemy教程**: https://docs.sqlalchemy.org/
- **OpenAI API**: https://platform.openai.com/docs/
- **Prometheus监控**: https://prometheus.io/docs/

---

**文档版本**: v2.0  
**最后更新**: 2025-12-16  
**维护者**: OpenWechatAI Team
