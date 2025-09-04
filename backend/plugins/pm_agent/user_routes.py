from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from database import get_db
from models import User
from schemas import UserCreate, UserUpdate, UserResponse, UserListResponse
from security import get_current_user, hash_password
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/", response_model=UserListResponse)
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of users to return"),
    role: Optional[str] = Query(None, description="Filter by role"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by username or email"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户列表
    
    支持分页、过滤和搜索功能
    """
    try:
        # 构建查询
        query = db.query(User)
        
        # 角色过滤
        if role:
            query = query.filter(User.role == role)
        
        # 状态过滤
        if status:
            query = query.filter(User.status == status)
        
        # 搜索过滤
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (User.username.ilike(search_filter)) |
                (User.email.ilike(search_filter))
            )
        
        # 获取总数
        total = query.count()
        
        # 分页查询
        users = query.offset(skip).limit(limit).all()
        
        return UserListResponse(
            users=users,
            total=total,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户列表失败"
        )

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建新用户
    
    只有管理员可以创建用户
    """
    try:
        # 检查权限
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有管理员可以创建用户"
            )
        
        # 检查用户名和邮箱是否已存在
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | 
            (User.email == user_data.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名或邮箱已存在"
            )
        
        # 创建新用户
        hashed_password = hash_password(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            role=user_data.role,
            status="active"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"用户 {user.username} 创建成功")
        return user
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"数据库完整性错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"创建用户失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建用户失败"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户详情
    
    用户只能查看自己的信息，管理员可以查看所有用户
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 权限检查
        if current_user.role != "admin" and str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户失败"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新用户信息
    
    用户可以更新自己的基本信息，管理员可以更新所有用户
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 权限检查
        if current_user.role != "admin" and str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        
        # 如果更新用户名或邮箱，检查重复
        if user_data.username and user_data.username != user.username:
            existing = db.query(User).filter(User.username == user_data.username).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已存在"
                )
            user.username = user_data.username
        
        if user_data.email and user_data.email != user.email:
            existing = db.query(User).filter(User.email == user_data.email).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已存在"
                )
            user.email = user_data.email
        
        # 更新密码
        if user_data.password:
            user.password_hash = hash_password(user_data.password)
        
        # 更新角色和状态（仅管理员）
        if current_user.role == "admin":
            if user_data.role:
                user.role = user_data.role
            if user_data.status:
                user.status = user_data.status
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"用户 {user.username} 更新成功")
        return user
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"数据库完整性错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"更新用户失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户失败"
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除用户
    
    只有管理员可以删除用户，且不能删除自己
    """
    try:
        # 权限检查
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有管理员可以删除用户"
            )
        
        if str(current_user.id) == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能删除自己"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        # 软删除：将状态设置为inactive而不是真正删除
        user.status = "inactive"
        db.commit()
        
        logger.info(f"用户 {user.username} 已停用")
        return {"message": f"用户 {user.username} 已停用"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除用户失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除用户失败"
        )

@router.get("/me/profile", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户信息
    """
    return current_user

@router.put("/me/profile", response_model=UserResponse)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息
    
    用户只能更新自己的基本信息，不能更新角色和状态
    """
    try:
        # 检查用户名重复
        if user_data.username and user_data.username != current_user.username:
            existing = db.query(User).filter(User.username == user_data.username).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已存在"
                )
            current_user.username = user_data.username
        
        # 检查邮箱重复
        if user_data.email and user_data.email != current_user.email:
            existing = db.query(User).filter(User.email == user_data.email).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已存在"
                )
            current_user.email = user_data.email
        
        # 更新密码
        if user_data.password:
            current_user.password_hash = hash_password(user_data.password)
        
        # 注意：普通用户不能更新role和status
        
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"用户 {current_user.username} 更新个人信息成功")
        return current_user
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"数据库完整性错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已存在"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"更新个人信息失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新个人信息失败"
        )
