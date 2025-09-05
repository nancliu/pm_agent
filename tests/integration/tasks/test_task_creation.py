"""
任务创建集成测试
"""

import httpx
import pytest
from datetime import datetime, timedelta
from backend.plugins.pm_agent.models import User, Task, TaskPriority, TaskStatus
from backend.plugins.pm_agent.security import hash_password
import uuid

base = "http://127.0.0.1:8000/api/pm_agent"


@pytest.fixture(scope="module", autouse=True)
def setup_test_data(db_session):
    """设置测试数据"""
    # 创建测试用户
    test_user = User(
        username="task_test_user",
        email="task_test@example.com",
        password_hash=hash_password("TestPassword123!"),
        role="member",
        status="active"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)
    
    # 创建另一个用户作为负责人
    assignee_user = User(
        username="task_assignee",
        email="assignee@example.com",
        password_hash=hash_password("TestPassword123!"),
        role="member",
        status="active"
    )
    db_session.add(assignee_user)
    db_session.commit()
    db_session.refresh(assignee_user)
    
    yield {
        "test_user": test_user,
        "assignee_user": assignee_user
    }
    
    # 清理测试数据
    db_session.query(Task).filter(Task.title.like("测试任务%")).delete()
    db_session.query(User).filter(User.username.in_(["task_test_user", "task_assignee"])).delete()
    db_session.commit()


def test_create_task_success(setup_test_data):
    """测试成功创建任务"""
    print("\n开始测试任务创建...")
    
    with httpx.Client(timeout=10.0) as client:
        # 1. 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_test_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. 创建任务
        task_data = {
            "title": "测试任务创建",
            "description": "这是一个测试任务描述",
            "assignee_id": str(setup_test_data["assignee_user"].id),
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "priority": "high"
        }
        
        create_response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert create_response.status_code == 201
        
        task_result = create_response.json()
        assert task_result["title"] == "测试任务创建"
        assert task_result["description"] == "这是一个测试任务描述"
        assert task_result["priority"] == "high"
        assert task_result["status"] == "pending"
        assert task_result["assignee_id"] == str(setup_test_data["assignee_user"].id)
        
        print("✅ 任务创建成功")


def test_create_task_without_assignee(setup_test_data):
    """测试创建任务时不指定负责人"""
    print("\n开始测试无负责人任务创建...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_test_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 创建任务（不指定负责人）
        task_data = {
            "title": "测试任务无负责人",
            "description": "这是一个没有负责人的测试任务",
            "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
            "priority": "medium"
        }
        
        create_response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert create_response.status_code == 201
        
        task_result = create_response.json()
        assert task_result["title"] == "测试任务无负责人"
        assert task_result["assignee_id"] is None
        assert task_result["priority"] == "medium"
        
        print("✅ 无负责人任务创建成功")


def test_create_task_validation_errors(setup_test_data):
    """测试任务创建验证错误"""
    print("\n开始测试任务创建验证错误...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_test_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 测试空标题
        task_data = {
            "title": "",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": "low"
        }
        response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert response.status_code == 422  # Validation error
        
        # 测试无效优先级
        task_data = {
            "title": "测试任务",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": "invalid_priority"
        }
        response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert response.status_code == 400
        
        # 测试不存在的负责人
        task_data = {
            "title": "测试任务",
            "assignee_id": str(uuid.uuid4()),
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": "low"
        }
        response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert response.status_code == 400
        
        print("✅ 任务创建验证错误测试通过")


def test_create_task_unauthorized():
    """测试未授权创建任务"""
    print("\n开始测试未授权任务创建...")
    
    with httpx.Client(timeout=10.0) as client:
        task_data = {
            "title": "未授权任务",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "priority": "low"
        }
        
        response = client.post(f"{base}/tasks", json=task_data)
        assert response.status_code == 401
        
        print("✅ 未授权任务创建测试通过")


def test_get_tasks_list(setup_test_data):
    """测试获取任务列表"""
    print("\n开始测试获取任务列表...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_test_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 获取任务列表
        response = client.get(f"{base}/tasks", headers=headers)
        assert response.status_code == 200
        
        tasks_data = response.json()
        assert "tasks" in tasks_data
        assert "total" in tasks_data
        assert "skip" in tasks_data
        assert "limit" in tasks_data
        assert isinstance(tasks_data["tasks"], list)
        
        print("✅ 获取任务列表测试通过")


def test_get_task_by_id(setup_test_data):
    """测试根据ID获取任务"""
    print("\n开始测试根据ID获取任务...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_test_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 先创建一个任务
        task_data = {
            "title": "测试获取任务",
            "description": "用于测试获取的任务",
            "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
            "priority": "medium"
        }
        
        create_response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]
        
        # 根据ID获取任务
        response = client.get(f"{base}/tasks/{task_id}", headers=headers)
        assert response.status_code == 200
        
        task_result = response.json()
        assert task_result["id"] == task_id
        assert task_result["title"] == "测试获取任务"
        
        print("✅ 根据ID获取任务测试通过")


if __name__ == "__main__":
    pytest.main([__file__])
