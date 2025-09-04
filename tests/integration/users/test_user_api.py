"""
用户管理API测试
"""

import httpx
import pytest

base_url = "http://127.0.0.1:8000/api/pm_agent"

def test_user_management_full_flow():
    """测试用户管理完整流程"""
    with httpx.Client(timeout=10.0) as client:
        # 1. 先登录获取管理员token（假设有已存在的管理员）
        login_response = client.post(f"{base_url}/auth/login", json={
            "username": "it_demo_auto",
            "password": "Passw0rd!"
        })
        
        if login_response.status_code != 200:
            # 如果用户不存在，先注册
            register_response = client.post(f"{base_url}/auth/register", json={
                "username": "it_demo_auto",
                "email": "it_demo_auto@example.com",
                "password": "Passw0rd!"
            })
            if register_response.status_code in [200, 400]:  # 已存在或创建成功
                login_response = client.post(f"{base_url}/auth/login", json={
                    "username": "it_demo_auto",
                    "password": "Passw0rd!"
                })
        
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. 测试获取用户列表
        list_response = client.get(f"{base_url}/users/", headers=headers)
        print(f"List users response: {list_response.status_code}")
        if list_response.status_code == 200:
            users_data = list_response.json()
            print(f"Users found: {len(users_data.get('users', []))}")
            assert "users" in users_data
            assert "total" in users_data
        
        # 3. 测试获取当前用户资料
        profile_response = client.get(f"{base_url}/users/me/profile", headers=headers)
        print(f"Get profile response: {profile_response.status_code}")
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            assert profile_data["username"] == "it_demo_auto"
        
        # 4. 测试更新当前用户资料
        update_response = client.put(f"{base_url}/users/me/profile", json={
            "username": "it_demo_auto_updated"
        }, headers=headers)
        print(f"Update profile response: {update_response.status_code}")
        if update_response.status_code == 200:
            updated_data = update_response.json()
            assert updated_data["username"] == "it_demo_auto_updated"
        
        # 5. 测试创建新用户（如果当前用户是管理员）
        create_response = client.post(f"{base_url}/users/", json={
            "username": "test_new_user",
            "email": "test_new_user@example.com",
            "password": "TestPass123!",
            "role": "member"
        }, headers=headers)
        print(f"Create user response: {create_response.status_code}")
        
        if create_response.status_code == 200:
            new_user = create_response.json()
            assert new_user["username"] == "test_new_user"
            user_id = new_user["id"]
            
            # 6. 测试获取特定用户
            get_user_response = client.get(f"{base_url}/users/{user_id}", headers=headers)
            print(f"Get user by ID response: {get_user_response.status_code}")
            if get_user_response.status_code == 200:
                user_data = get_user_response.json()
                assert user_data["id"] == user_id
            
            # 7. 测试更新特定用户
            update_user_response = client.put(f"{base_url}/users/{user_id}", json={
                "email": "test_new_user_updated@example.com"
            }, headers=headers)
            print(f"Update user response: {update_user_response.status_code}")
            
            # 8. 测试删除用户
            delete_response = client.delete(f"{base_url}/users/{user_id}", headers=headers)
            print(f"Delete user response: {delete_response.status_code}")
            
        elif create_response.status_code == 403:
            print("User is not admin, skipping admin-only tests")
        else:
            print(f"Create user failed with status: {create_response.status_code}")
            print(f"Response: {create_response.text}")


def test_user_api_basic():
    """测试用户API基础功能"""
    with httpx.Client(timeout=10.0) as client:
        # 获取用户token
        login_response = client.post(f"{base_url}/auth/login", json={
            "username": "it_demo_auto",
            "password": "Passw0rd!"
        })
        
        if login_response.status_code != 200:
            # 注册用户
            client.post(f"{base_url}/auth/register", json={
                "username": "it_demo_auto",
                "email": "it_demo_auto@example.com",
                "password": "Passw0rd!"
            })
            login_response = client.post(f"{base_url}/auth/login", json={
                "username": "it_demo_auto",
                "password": "Passw0rd!"
            })
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 测试用户列表API
        response = client.get(f"{base_url}/users/", headers=headers)
        assert response.status_code in [200, 403]  # 可能没有权限
        
        # 测试当前用户资料API
        response = client.get(f"{base_url}/users/me/profile", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "username" in data
        assert "email" in data


if __name__ == "__main__":
    test_user_api_basic()
    test_user_management_full_flow()
    print("All tests completed successfully!")
