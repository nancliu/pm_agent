import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 测试导入路径
ROOT = os.path.dirname(os.path.dirname(__file__))
PLUGIN_DIR = os.path.join(ROOT, 'backend', 'plugins', 'pm_agent')
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if PLUGIN_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_DIR)

# 禁用代理，确保本地请求直连
for key in [
    'HTTP_PROXY', 'HTTPS_PROXY', 'FTP_PROXY',
    'http_proxy', 'https_proxy', 'ftp_proxy'
]:
    os.environ.pop(key, None)

os.environ['NO_PROXY'] = 'localhost,127.0.0.1,0.0.0.0'

# 导入后端模块
from backend.plugins.pm_agent.database import Base
from backend.plugins.pm_agent.config import settings

# 测试数据库配置
TEST_DATABASE_URL = settings.DATABASE_URL.replace("pm_agent", "pm_agent_test")
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """设置测试数据库"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def db_session():
    """提供数据库会话"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def base_url():
    """基础URL"""
    return "http://127.0.0.1:8000/api/pm_agent"
