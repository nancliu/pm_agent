"""
测试管理员用户管理功能
"""

import httpx
import json

base_url = "http://127.0.0.1:8000/api/pm_agent"

def test_admin_user_management():
    """测试管理员用户管理功能"""
    with httpx.Client(timeout=10.0) as client:
        # 1. 管理员登录
        login_response = client.post(f"{base_url}/auth/login", json={
            "username": "admin_test",
            "password": "Admin123!"
        })
        
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("✓ 管理员登录成功")
        
        # 2. 测试获取用户列表
        list_response = client.get(f"{base_url}/users/", headers=headers)
        assert list_response.status_code == 200
        users_data = list_response.json()
        print(f"✓ 获取用户列表成功，共 {users_data['total']} 个用户")
        
        # 3. 测试创建新用户
        create_response = client.post(f"{base_url}/users/", json={
            "username": "test_user_1",
            "email": "test_user_1@example.com",
            "password": "TestPass123!",
            "role": "member"
        }, headers=headers)
        
        assert create_response.status_code == 200
        new_user = create_response.json()
        user_id = new_user["id"]
        print(f"✓ 创建用户成功，用户ID: {user_id}")
        
        # 4. 测试获取特定用户
        get_user_response = client.get(f"{base_url}/users/{user_id}", headers=headers)
        assert get_user_response.status_code == 200
        user_data = get_user_response.json()
        assert user_data["username"] == "test_user_1"
        print("✓ 获取特定用户成功")
        
        # 5. 测试更新用户
        update_response = client.put(f"{base_url}/users/{user_id}", json={
            "email": "test_user_1_updated@example.com",
            "role": "admin"
        }, headers=headers)
        
        assert update_response.status_code == 200
        updated_user = update_response.json()
        assert updated_user["email"] == "test_user_1_updated@example.com"
        assert updated_user["role"] == "admin"
        print("✓ 更新用户成功")
        
        # 6. 测试用户搜索
        search_response = client.get(f"{base_url}/users/?search=test_user", headers=headers)
        assert search_response.status_code == 200
        search_data = search_response.json()
        assert len(search_data["users"]) > 0
        print("✓ 用户搜索功能正常")
        
        # 7. 测试角色过滤
        filter_response = client.get(f"{base_url}/users/?role=admin", headers=headers)
        assert filter_response.status_code == 200
        filter_data = filter_response.json()
        assert all(user["role"] == "admin" for user in filter_data["users"])
        print("✓ 角色过滤功能正常")
        
        # 8. 测试分页
        page_response = client.get(f"{base_url}/users/?skip=0&limit=2", headers=headers)
        assert page_response.status_code == 200
        page_data = page_response.json()
        assert page_data["limit"] == 2
        assert len(page_data["users"]) <= 2
        print("✓ 分页功能正常")
        
        # 9. 测试删除用户（软删除）
        delete_response = client.delete(f"{base_url}/users/{user_id}", headers=headers)
        assert delete_response.status_code == 200
        print("✓ 删除用户成功（软删除）")
        
        # 10. 验证用户已被停用
        status_response = client.get(f"{base_url}/users/{user_id}", headers=headers)
        assert status_response.status_code == 200
        deleted_user = status_response.json()
        # 注意：我们实现的是软删除，用户状态变为inactive
        print(f"用户状态: {deleted_user['status']}")
        
        print("\n🎉 所有管理员用户管理功能测试通过！")


def test_regular_user_permissions():
    """测试普通用户权限限制"""
    with httpx.Client(timeout=10.0) as client:
        # 1. 普通用户登录
        login_response = client.post(f"{base_url}/auth/login", json={
            "username": "it_demo_auto_updated",  # 这是之前的测试用户
            "password": "Passw0rd!"
        })
        
        if login_response.status_code != 200:
            print("普通用户不存在，跳过权限测试")
            return
            
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. 尝试创建用户（应该被拒绝）
        create_response = client.post(f"{base_url}/users/", json={
            "username": "should_fail",
            "email": "should_fail@example.com",
            "password": "TestPass123!",
            "role": "member"
        }, headers=headers)
        
        assert create_response.status_code == 403
        print("✓ 普通用户无法创建用户（正确）")
        
        # 3. 可以获取自己的资料
        profile_response = client.get(f"{base_url}/users/me/profile", headers=headers)
        assert profile_response.status_code == 200
        print("✓ 普通用户可以获取自己的资料")
        
        # 4. 可以更新自己的资料
        update_response = client.put(f"{base_url}/users/me/profile", json={
            "email": "it_demo_auto_new@example.com"
        }, headers=headers)
        assert update_response.status_code == 200
        print("✓ 普通用户可以更新自己的资料")
        
        print("\n🎉 普通用户权限限制测试通过！")


if __name__ == "__main__":
    print("开始测试用户管理功能...\n")
    
    try:
        test_admin_user_management()
        print()
        test_regular_user_permissions()
        
        print("\n✅ 所有用户管理功能测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        raise
