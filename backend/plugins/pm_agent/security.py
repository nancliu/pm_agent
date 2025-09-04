"""
认证与安全工具：密码哈希、JWT令牌、当前用户依赖
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/pm_agent/auth/login")


def hash_password(plain_password: str) -> str:
    """对明文密码进行哈希。"""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """校验明文密码与哈希是否匹配。"""
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    """生成JWT访问令牌。"""
    expire_delta = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """解码并验证JWT令牌。失败返回None。"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """基于JWT的当前用户依赖。"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效或过期的凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    subject: Optional[str] = payload.get("sub") if isinstance(payload, dict) else None
    if subject is None:
        raise credentials_exception

    user = db.query(User).filter(User.id.cast(str) == subject).first()
    if not user:
        # 兼容sub为用户名
        user = db.query(User).filter(User.username == subject).first()
    if not user:
        raise credentials_exception

    return user
