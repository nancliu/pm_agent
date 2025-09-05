"""
任务模型单元测试
"""

import pytest
from datetime import datetime, timedelta
from backend.plugins.pm_agent.models import Task, TaskPriority, TaskStatus
from backend.plugins.pm_agent.schemas import TaskCreate, TaskUpdate, TaskResponse
import uuid


def test_task_priority_enum():
    """测试任务优先级枚举"""
    assert TaskPriority.HIGH.value == "high"
    assert TaskPriority.MEDIUM.value == "medium"
    assert TaskPriority.LOW.value == "low"


def test_task_status_enum():
    """测试任务状态枚举"""
    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus.IN_PROGRESS.value == "in_progress"
    assert TaskStatus.COMPLETED.value == "completed"
    assert TaskStatus.BLOCKED.value == "blocked"


def test_task_create_schema():
    """测试任务创建模式"""
    task_data = {
        "title": "测试任务",
        "description": "这是一个测试任务",
        "assignee_id": uuid.uuid4(),
        "due_date": datetime.now() + timedelta(days=7),
        "priority": "high"
    }
    
    task = TaskCreate(**task_data)
    assert task.title == "测试任务"
    assert task.description == "这是一个测试任务"
    assert task.priority == "high"


def test_task_create_schema_validation():
    """测试任务创建模式验证"""
    # 测试必填字段
    with pytest.raises(ValueError):
        TaskCreate(title="", due_date=datetime.now())
    
    # 测试标题长度限制
    with pytest.raises(ValueError):
        TaskCreate(title="x" * 101, due_date=datetime.now())
    
    # 测试描述长度限制
    with pytest.raises(ValueError):
        TaskCreate(
            title="测试任务",
            description="x" * 501,
            due_date=datetime.now()
        )


def test_task_update_schema():
    """测试任务更新模式"""
    update_data = {
        "title": "更新的任务标题",
        "priority": "low"
    }
    
    task_update = TaskUpdate(**update_data)
    assert task_update.title == "更新的任务标题"
    assert task_update.priority == "low"
    assert task_update.description is None


def test_task_response_schema():
    """测试任务响应模式"""
    task_data = {
        "id": uuid.uuid4(),
        "title": "测试任务",
        "description": "这是一个测试任务",
        "assignee_id": uuid.uuid4(),
        "due_date": datetime.now() + timedelta(days=7),
        "priority": "high",
        "status": "pending",
        "created_by": uuid.uuid4(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    }
    
    task_response = TaskResponse(**task_data)
    assert task_response.id == task_data["id"]
    assert task_response.title == "测试任务"
    assert task_response.status == "pending"
