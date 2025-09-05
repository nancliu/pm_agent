"""
任务管理集成测试（更新、删除）
"""

import httpx
import pytest
from datetime import datetime, timedelta
from backend.plugins.pm_agent.models import User, Task
from backend.plugins.pm_agent.security import hash_password
import uuid

base = "http://127.0.0.1:8000/api/pm_agent"


@pytest.fixture(scope="module", autouse=True)
def setup_test_data(db_session):
    """设置测试数据"""
    # 创建测试用户
    test_user = User(
        username="task_mgmt_user",
        email="task_mgmt@example.com",
        password_hash=hash_password("TestPassword123!"),
        role="member",
        status="active"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)
    
    # 创建另一个用户作为负责人
    assignee_user = User(
        username="task_mgmt_assignee",
        email="mgmt_assignee@example.com",
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
    db_session.query(Task).filter(Task.title.like("管理测试任务%")).delete()
    db_session.query(User).filter(User.username.in_(["task_mgmt_user", "task_mgmt_assignee"])).delete()
    db_session.commit()


def test_update_task_success(setup_test_data):
    """测试成功更新任务"""
    print("\n开始测试任务更新...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_mgmt_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 先创建一个任务
        task_data = {
            "title": "管理测试任务原始",
            "description": "原始描述",
            "assignee_id": str(setup_test_data["assignee_user"].id),
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "priority": "low"
        }
        
        create_response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]
        
        # 更新任务
        update_data = {
            "title": "管理测试任务已更新",
            "description": "更新后的描述",
            "priority": "high",
            "status": "in_progress"
        }
        
        update_response = client.put(f"{base}/tasks/{task_id}", json=update_data, headers=headers)
        assert update_response.status_code == 200
        
        updated_task = update_response.json()
        assert updated_task["title"] == "管理测试任务已更新"
        assert updated_task["description"] == "更新后的描述"
        assert updated_task["priority"] == "high"
        assert updated_task["status"] == "in_progress"
        
        print("✅ 任务更新成功")


def test_update_task_partial(setup_test_data):
    """测试部分更新任务"""
    print("\n开始测试任务部分更新...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_mgmt_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 先创建一个任务
        task_data = {
            "title": "管理测试任务部分更新",
            "description": "原始描述",
            "due_date": (datetime.now() + timedelta(days=5)).isoformat(),
            "priority": "medium"
        }
        
        create_response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]
        
        # 只更新标题
        update_data = {
            "title": "管理测试任务部分更新完成"
        }
        
        update_response = client.put(f"{base}/tasks/{task_id}", json=update_data, headers=headers)
        assert update_response.status_code == 200
        
        updated_task = update_response.json()
        assert updated_task["title"] == "管理测试任务部分更新完成"
        assert updated_task["description"] == "原始描述"  # 未更新的字段保持不变
        assert updated_task["priority"] == "medium"
        
        print("✅ 任务部分更新成功")


def test_update_task_validation_errors(setup_test_data):
    """测试任务更新验证错误"""
    print("\n开始测试任务更新验证错误...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_mgmt_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 先创建一个任务
        task_data = {
            "title": "管理测试任务验证",
            "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
            "priority": "low"
        }
        
        create_response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]
        
        # 测试无效优先级
        update_data = {
            "priority": "invalid_priority"
        }
        response = client.put(f"{base}/tasks/{task_id}", json=update_data, headers=headers)
        assert response.status_code == 400
        
        # 测试无效状态
        update_data = {
            "status": "invalid_status"
        }
        response = client.put(f"{base}/tasks/{task_id}", json=update_data, headers=headers)
        assert response.status_code == 400
        
        # 测试不存在的负责人
        update_data = {
            "assignee_id": str(uuid.uuid4())
        }
        response = client.put(f"{base}/tasks/{task_id}", json=update_data, headers=headers)
        assert response.status_code == 400
        
        print("✅ 任务更新验证错误测试通过")


def test_update_nonexistent_task(setup_test_data):
    """测试更新不存在的任务"""
    print("\n开始测试更新不存在任务...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_mgmt_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 尝试更新不存在的任务
        fake_task_id = str(uuid.uuid4())
        update_data = {
            "title": "不存在的任务"
        }
        
        response = client.put(f"{base}/tasks/{fake_task_id}", json=update_data, headers=headers)
        assert response.status_code == 404
        
        print("✅ 更新不存在任务测试通过")


def test_delete_task_success(setup_test_data):
    """测试成功删除任务"""
    print("\n开始测试任务删除...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_mgmt_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 先创建一个任务
        task_data = {
            "title": "管理测试任务删除",
            "description": "将被删除的任务",
            "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
            "priority": "low"
        }
        
        create_response = client.post(f"{base}/tasks", json=task_data, headers=headers)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]
        
        # 删除任务
        delete_response = client.delete(f"{base}/tasks/{task_id}", headers=headers)
        assert delete_response.status_code == 204
        
        # 验证任务已被软删除（无法通过正常查询获取）
        get_response = client.get(f"{base}/tasks/{task_id}", headers=headers)
        assert get_response.status_code == 404
        
        print("✅ 任务删除成功")


def test_delete_nonexistent_task(setup_test_data):
    """测试删除不存在的任务"""
    print("\n开始测试删除不存在任务...")
    
    with httpx.Client(timeout=10.0) as client:
        # 登录获取token
        login_response = client.post(f"{base}/auth/login", json={
            "username": "task_mgmt_user",
            "password": "TestPassword123!"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 尝试删除不存在的任务
        fake_task_id = str(uuid.uuid4())
        response = client.delete(f"{base}/tasks/{fake_task_id}", headers=headers)
        assert response.status_code == 404
        
        print("✅ 删除不存在任务测试通过")


def test_task_operations_unauthorized():
    """测试未授权的任务操作"""
    print("\n开始测试未授权任务操作...")
    
    with httpx.Client(timeout=10.0) as client:
        fake_task_id = str(uuid.uuid4())
        
        # 测试未授权获取任务
        response = client.get(f"{base}/tasks/{fake_task_id}")
        assert response.status_code == 401
        
        # 测试未授权更新任务
        response = client.put(f"{base}/tasks/{fake_task_id}", json={"title": "未授权更新"})
        assert response.status_code == 401
        
        # 测试未授权删除任务
        response = client.delete(f"{base}/tasks/{fake_task_id}")
        assert response.status_code == 401
        
        print("✅ 未授权任务操作测试通过")


if __name__ == "__main__":
    pytest.main([__file__])
