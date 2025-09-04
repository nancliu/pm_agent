"""
数据库连接测试
"""

import pytest
from sqlalchemy import create_engine, text
from backend.plugins.pm_agent.config import settings


def test_database_connection():
    """测试数据库连接"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
        print("✅ 数据库连接测试通过")
    except Exception as e:
        pytest.fail(f"数据库连接失败: {e}")


def test_database_tables_exist():
    """测试数据库表是否存在"""
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
            assert result.scalar() == True, "用户表不存在"
            
            # 检查任务表
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'tasks'
                );
            """))
            assert result.scalar() == True, "任务表不存在"
            
            # 检查任务历史表
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'task_history'
                );
            """))
            assert result.scalar() == True, "任务历史表不存在"
        
        print("✅ 数据库表存在性测试通过")
    except Exception as e:
        pytest.fail(f"数据库表检查失败: {e}")


def test_database_extensions():
    """测试数据库扩展是否启用"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            # 检查uuid-ossp扩展
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 FROM pg_extension 
                    WHERE extname = 'uuid-ossp'
                );
            """))
            assert result.scalar() == True, "uuid-ossp扩展未启用"
            
            # 检查pgcrypto扩展
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 FROM pg_extension 
                    WHERE extname = 'pgcrypto'
                );
            """))
            assert result.scalar() == True, "pgcrypto扩展未启用"
        
        print("✅ 数据库扩展测试通过")
    except Exception as e:
        pytest.fail(f"数据库扩展检查失败: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
