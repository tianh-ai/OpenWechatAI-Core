"""
测试配置和通用fixtures
"""
import pytest
from unittest.mock import Mock, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base


@pytest.fixture(scope="session")
def test_database():
    """测试数据库"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    TestingSessionLocal = sessionmaker(bind=engine)
    
    yield TestingSessionLocal
    
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(test_database):
    """数据库会话"""
    session = test_database()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def mock_wechat_device():
    """模拟微信设备"""
    device = MagicMock()
    device.info = {"serial": "test_device"}
    device.app_info.return_value = {"packageName": "com.tencent.mm"}
    return device


@pytest.fixture
def mock_ai_router():
    """模拟AI路由器"""
    router = Mock()
    router.chat.return_value = Mock(
        content="AI回复内容",
        model="gpt-3.5-turbo",
        tokens_used=100,
        finish_reason="stop",
        cost=0.001
    )
    return router


@pytest.fixture
def sample_message():
    """示例消息"""
    return {
        "platform": "wechat",
        "sender": "test_user",
        "receiver": "bot",
        "content": "测试消息",
        "type": "text",
        "timestamp": 1234567890
    }
