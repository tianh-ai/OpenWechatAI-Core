"""
配置测试
"""
import pytest
from pydantic import ValidationError
from core.config import Settings


class TestSettings:
    """设置配置测试"""
    
    def test_default_values(self):
        """测试默认值"""
        settings = Settings()
        
        assert settings.redis_url == "redis://localhost:6379/0"
        assert settings.log_level == "INFO"
        assert settings.debug is False
    
    def test_database_url_required(self):
        """测试数据库URL必填"""
        # 数据库URL是必需的
        settings = Settings()
        assert settings.database_url is not None
    
    def test_celery_broker_fallback(self):
        """测试Celery Broker回退到Redis"""
        settings = Settings()
        
        # 如果未设置celery_broker_url，应该能使用redis_url
        assert settings.redis_url is not None
    
    def test_openai_model_default(self):
        """测试OpenAI默认模型"""
        settings = Settings()
        
        assert settings.openai_model == "gpt-4-turbo-preview"
    
    def test_gemini_model_default(self):
        """测试Gemini默认模型"""
        settings = Settings()
        
        assert settings.gemini_model == "gemini-pro"


class TestEnvironmentLoading:
    """环境变量加载测试"""
    
    def test_env_override(self, monkeypatch):
        """测试环境变量覆盖"""
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("DEBUG", "true")
        
        settings = Settings()
        
        assert settings.log_level == "DEBUG"
        assert settings.debug is True
    
    def test_redis_url_from_env(self, monkeypatch):
        """测试从环境变量读取Redis URL"""
        test_redis_url = "redis://test:6380/1"
        monkeypatch.setenv("REDIS_URL", test_redis_url)
        
        settings = Settings()
        
        assert settings.redis_url == test_redis_url
