"""
1.2 安全工具单元测试：密码哈希与JWT
"""

import os
import sys
from datetime import timedelta

# 允许导入插件代码
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend", "plugins", "pm_agent"))

from security import hash_password, verify_password, create_access_token, decode_token  # type: ignore
from config import settings  # type: ignore


def test_password_hash_and_verify():
    raw = "Passw0rd!"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_create_and_decode():
    token = create_access_token("tester", expires_minutes=1)
    payload = decode_token(token)
    assert payload is not None
    assert payload.get("sub") == "tester"


def test_jwt_short_expiry():
    token = create_access_token("tester2", expires_minutes=0)
    # 0分钟的token可能立刻过期；至少可被解码（是否过期由调用方判断），这里仅校验结构
    payload = decode_token(token)
    assert payload is not None
