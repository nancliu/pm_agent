"""
项目管理 Agent 数据库模块
"""

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

# 创建元数据对象
metadata = MetaData()


async def init_db():
    """初始化数据库连接"""
    try:
        # 测试数据库连接
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("数据库连接成功")
        return True
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return False


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 数据库健康检查
async def check_db_health():
    """检查数据库健康状态"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"status": "healthy", "message": "数据库连接正常"}
    except Exception as e:
        return {"status": "unhealthy", "message": f"数据库连接异常: {e}"}
