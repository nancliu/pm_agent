"""
用户管理集成测试
"""

import httpx
import pytest
from backend.plugins.pm_agent.models import User, UserRole, UserStatus
from backend.plugins.pm_agent.security import hash_password


@pytest.fixture(scope="module", autouse=True)
def setup_test_users(db_session):
    """设置测试用户"""
    # 清理测试用户
    test_usernames = ["admin_test", "user_test_1", "user_test_2", "user_to_update", "user_to_delete"]
    for username in test_usernames:
        db_session.query(User).filter(User.username == username).delete()
    db_session.commit()
    
    # 创建管理员测试用户
    admin_user = User(
        username="admin_test",
        email="admin_test@example.com",
        password_hash=hash_password("Admin123!"),
        role="admin",
        status="active"
    )
    db_session.add(admin_user)
    db_session.commit()
    
    yield
    
    # 清理测试用户
    for username in test_usernames:
        db_session.query(User).filter(User.username == username).delete()
    db_session.commit()


@pytest.fixture
def admin_token():
    """获取管理员token"""
    with httpx.Client(timeout=10.0) as client:
        response = client.post("http://127.0.0.1:8000/api/pm_agent/auth/login", json={
            "username": "admin_test",
            "password": "Admin123!"
        })
        assert response.status_code == 200
        return response.json()["access_token"]


@pytest.fixture
def regular_user_token():
    """创建并获取普通用户token"""
    with httpx.Client(timeout=10.0) as client:
        # 先用管理员创建用户
        admin_response = client.post("http://127.0.0.1:8000/api/pm_agent/auth/login", json={
            "username": "admin_test",
            "password": "Admin123!"
        })
        admin_token = admin_response.json()["access_token"]
        
        # 创建普通用户
        client.post(
            "http://127.0.0.1:8000/api/pm_agent/users/",
            json={
                "username": "user_test_1",
                "email": "user_test_1@example.com",
                "password": "User123!",
                "role": "member"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        # 获取普通用户token
        user_response = client.post("http://127.0.0.1:8000/api/pm_agent/auth/login", json={
            "username": "user_test_1",
            "password": "User123!"
        })
        return user_response.json()["access_token"]


def test_create_user_as_admin(admin_token):
    """测试管理员创建用户"""
    with httpx.Client(timeout=10.0) as client:
        response = client.post(
            "http://127.0.0.1:8000/api/pm_agent/users/",
            json={
                "username": "user_test_2",
                "email": "user_test_2@example.com",
                "password": "User123!",
                "role": "member"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["username"] == "user_test_2"
        assert user_data["email"] == "user_test_2@example.com"
        assert user_data["role"] == "member"
        assert user_data["status"] == "active"
        assert "password_hash" not in user_data  # 密码不应该返回


def test_create_user_as_regular_user_forbidden(regular_user_token):
    """测试普通用户不能创建用户"""
    with httpx.Client(timeout=10.0) as client:
        response = client.post(
            "http://127.0.0.1:8000/api/pm_agent/users/",
            json={
                "username": "should_not_work",
                "email": "should_not_work@example.com",
                "password": "Password123!",
                "role": "member"
            },
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        
        assert response.status_code == 403
        assert "只有管理员可以创建用户" in response.json()["detail"]


def test_create_user_duplicate_username(admin_token):
    """测试创建重复用户名的用户"""
    with httpx.Client(timeout=10.0) as client:
        response = client.post(
            "http://127.0.0.1:8000/api/pm_agent/users/",
            json={
                "username": "admin_test",  # 已存在的用户名
                "email": "new_email@example.com",
                "password": "Password123!",
                "role": "member"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 400
        assert "用户名或邮箱已存在" in response.json()["detail"]


def test_list_users(admin_token):
    """测试获取用户列表"""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            "http://127.0.0.1:8000/api/pm_agent/users/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
        assert len(data["users"]) > 0
        
        # 验证返回的用户包含必要字段
        user = data["users"][0]
        assert "id" in user
        assert "username" in user
        assert "email" in user
        assert "role" in user
        assert "status" in user


def test_list_users_with_filters(admin_token):
    """测试带过滤条件的用户列表"""
    with httpx.Client(timeout=10.0) as client:
        # 按角色过滤
        response = client.get(
            "http://127.0.0.1:8000/api/pm_agent/users/?role=admin",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(user["role"] == "admin" for user in data["users"])
        
        # 按状态过滤
        response = client.get(
            "http://127.0.0.1:8000/api/pm_agent/users/?status=active",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(user["status"] == "active" for user in data["users"])
        
        # 搜索功能
        response = client.get(
            "http://127.0.0.1:8000/api/pm_agent/users/?search=admin",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert any("admin" in user["username"].lower() or "admin" in user["email"].lower() 
                  for user in data["users"])


def test_get_user_by_id(admin_token, db_session):
    """测试根据ID获取用户"""
    # 获取一个已存在的用户ID
    user = db_session.query(User).filter(User.username == "admin_test").first()
    user_id = str(user.id)
    
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            f"http://127.0.0.1:8000/api/pm_agent/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "admin_test"


def test_get_user_not_found(admin_token):
    """测试获取不存在的用户"""
    fake_id = "550e8400-e29b-41d4-a716-446655440000"
    
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            f"http://127.0.0.1:8000/api/pm_agent/users/{fake_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 404
        assert "用户不存在" in response.json()["detail"]


def test_update_user(admin_token, db_session):
    """测试更新用户信息"""
    # 先创建一个用户用于更新
    with httpx.Client(timeout=10.0) as client:
        create_response = client.post(
            "http://127.0.0.1:8000/api/pm_agent/users/",
            json={
                "username": "user_to_update",
                "email": "user_to_update@example.com",
                "password": "User123!",
                "role": "member"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        user_id = create_response.json()["id"]
        
        # 更新用户信息
        update_response = client.put(
            f"http://127.0.0.1:8000/api/pm_agent/users/{user_id}",
            json={
                "username": "user_updated",
                "email": "user_updated@example.com",
                "role": "admin"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["username"] == "user_updated"
        assert data["email"] == "user_updated@example.com"
        assert data["role"] == "admin"


def test_update_user_insufficient_permission(regular_user_token, db_session):
    """测试普通用户不能更新其他用户"""
    # 获取admin用户的ID
    admin_user = db_session.query(User).filter(User.username == "admin_test").first()
    admin_id = str(admin_user.id)
    
    with httpx.Client(timeout=10.0) as client:
        response = client.put(
            f"http://127.0.0.1:8000/api/pm_agent/users/{admin_id}",
            json={"username": "hacked_admin"},
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        
        assert response.status_code == 403
        assert "权限不足" in response.json()["detail"]


def test_delete_user(admin_token, db_session):
    """测试删除用户（软删除）"""
    # 先创建一个用户用于删除
    with httpx.Client(timeout=10.0) as client:
        create_response = client.post(
            "http://127.0.0.1:8000/api/pm_agent/users/",
            json={
                "username": "user_to_delete",
                "email": "user_to_delete@example.com",
                "password": "User123!",
                "role": "member"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        user_id = create_response.json()["id"]
        
        # 删除用户
        delete_response = client.delete(
            f"http://127.0.0.1:8000/api/pm_agent/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert delete_response.status_code == 200
        assert "已停用" in delete_response.json()["message"]
        
        # 验证用户状态变为inactive
        user = db_session.query(User).filter(User.id == user_id).first()
        assert user.status == "inactive"


def test_delete_self_forbidden(admin_token, db_session):
    """测试不能删除自己"""
    # 获取当前管理员用户的ID
    admin_user = db_session.query(User).filter(User.username == "admin_test").first()
    admin_id = str(admin_user.id)
    
    with httpx.Client(timeout=10.0) as client:
        response = client.delete(
            f"http://127.0.0.1:8000/api/pm_agent/users/{admin_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 400
        assert "不能删除自己" in response.json()["detail"]


def test_get_current_user_profile(regular_user_token):
    """测试获取当前用户资料"""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            "http://127.0.0.1:8000/api/pm_agent/users/me/profile",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "user_test_1"
        assert data["email"] == "user_test_1@example.com"
        assert data["role"] == "member"


def test_update_current_user_profile(regular_user_token):
    """测试更新当前用户资料"""
    with httpx.Client(timeout=10.0) as client:
        response = client.put(
            "http://127.0.0.1:8000/api/pm_agent/users/me/profile",
            json={
                "username": "user_test_1_updated",
                "email": "user_test_1_updated@example.com"
            },
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "user_test_1_updated"
        assert data["email"] == "user_test_1_updated@example.com"
        # 角色和状态不应该被普通用户更改
        assert data["role"] == "member"


def test_user_pagination(admin_token):
    """测试用户列表分页"""
    with httpx.Client(timeout=10.0) as client:
        # 测试分页参数
        response = client.get(
            "http://127.0.0.1:8000/api/pm_agent/users/?skip=0&limit=1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["skip"] == 0
        assert data["limit"] == 1
        assert len(data["users"]) <= 1
        assert data["total"] >= 1
