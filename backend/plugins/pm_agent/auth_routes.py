"""
认证路由：注册、登录、获取当前用户、退出
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import RegisterRequest, LoginRequest, TokenResponse, MeResponse
from security import hash_password, verify_password, create_access_token, get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MeResponse)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user: Optional[User] = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=MeResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout():
    # 占位：JWT为无状态，前端删除token或服务端维护黑名单
    return {"message": "已退出（占位）"}
