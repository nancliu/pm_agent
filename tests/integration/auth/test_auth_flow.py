"""
1.2 认证流程集成测试
"""

import os
import sys
import httpx

base = "http://localhost:8000/api/pm_agent"


def test_auth_register_login_me():
    with httpx.Client(timeout=10.0) as s:
        # 注册（重复注册允许返回400）
        r = s.post(f"{base}/auth/register", json={
            "username": "it_demo_auto",
            "email": "it_demo_auto@example.com",
            "password": "Passw0rd!"
        })
        assert r.status_code in (200, 400)

        # 登录
        r = s.post(f"{base}/auth/login", json={
            "username": "it_demo_auto",
            "password": "Passw0rd!"
        })
        assert r.status_code == 200
        tok = r.json().get("access_token")
        assert tok

        # 我
        r = s.get(f"{base}/auth/me", headers={"Authorization": f"Bearer {tok}"})
        assert r.status_code == 200
        data = r.json()
        assert data.get("username") == "it_demo_auto"
