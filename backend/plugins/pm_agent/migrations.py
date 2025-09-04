"""
项目管理 Agent 数据库迁移脚本
"""

from sqlalchemy import create_engine, text
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from models import Base
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    """创建所有表"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        return True
    except Exception as e:
        logger.error(f"数据库表创建失败: {e}")
        return False


def drop_tables():
    """删除所有表"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.drop_all(bind=engine)
        logger.info("数据库表删除成功")
        return True
    except Exception as e:
        logger.error(f"数据库表删除失败: {e}")
        return False


def check_tables():
    """检查表是否存在"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            # 检查用户表
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'users'
                );
            """))
            users_exists = result.scalar()
            
            # 检查任务表
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'tasks'
                );
            """))
            tasks_exists = result.scalar()
            
            # 检查任务历史表
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'task_history'
                );
            """))
            history_exists = result.scalar()
            
            return {
                "users": users_exists,
                "tasks": tasks_exists,
                "task_history": history_exists
            }
    except Exception as e:
        logger.error(f"检查表失败: {e}")
        return None


if __name__ == "__main__":
    # 运行迁移
    print("开始数据库迁移...")
    
    # 检查现有表
    tables = check_tables()
    if tables:
        print(f"现有表状态: {tables}")
    
    # 创建表
    if create_tables():
        print("数据库迁移完成")
    else:
        print("数据库迁移失败")
