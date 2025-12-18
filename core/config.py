from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Manages application settings using Pydantic v2.
    Reads from environment variables (case-insensitive).
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # MCP数据库配置（替代直接数据库连接）
    mcp_database_endpoint: Optional[str] = Field(
        default=None,
        description="MCP数据库服务端点 (例: http://localhost:3000/mcp)"
    )
    mcp_database_api_key: Optional[str] = Field(
        default=None,
        description="MCP数据库API密钥"
    )
    mcp_database_timeout: int = Field(
        default=30,
        description="MCP数据库请求超时（秒）"
    )
    
    # Redis配置
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis连接URL"
    )
    
    # Celery配置
    celery_broker_url: Optional[str] = Field(
        default=None,
        description="Celery Broker URL，默认使用redis_url"
    )
    celery_result_backend: Optional[str] = Field(
        default=None,
        description="Celery Result Backend，默认使用redis_url"
    )
    
    # AI API Keys
    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API密钥"
    )
    openai_model: str = Field(
        default="gpt-4-turbo-preview",
        description="默认使用的OpenAI模型"
    )
    
    # Gemini配置
    gemini_api_key: Optional[str] = Field(
        default=None,
        description="Google Gemini API密钥"
    )
    gemini_model: str = Field(
        default="gemini-pro",
        description="默认使用的Gemini模型"
    )
    
    # 日志配置
    log_level: str = Field(
        default="INFO",
        description="日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    log_file: str = Field(
        default="logs/app.log",
        description="日志文件路径"
    )
    
    # 应用配置
    debug: bool = Field(
        default=False,
        description="调试模式"
    )
    environment: str = Field(
        default="development",
        description="运行环境: development, staging, production"
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 自动设置Celery配置
        if not self.celery_broker_url:
            self.celery_broker_url = self.redis_url.replace("/0", "/1")
        if not self.celery_result_backend:
            self.celery_result_backend = self.redis_url.replace("/0", "/2")

# Create a single instance of the settings to be used throughout the application
settings = Settings()
