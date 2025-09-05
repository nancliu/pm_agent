"""
权限控制模块
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User, Task, UserRole
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def check_task_edit_permission(
    current_user: User, 
    task: Task, 
    db: Session
) -> bool:
    """
    检查用户是否有权限编辑任务
    
    Args:
        current_user: 当前用户
        task: 要编辑的任务
        db: 数据库会话
        
    Returns:
        bool: 是否有权限编辑
        
    Raises:
        HTTPException: 权限不足时抛出异常
    """
    # 管理员可以编辑所有任务
    if current_user.role == UserRole.ADMIN.value:
        return True
    
    # 项目经理可以编辑所有任务
    if current_user.role == UserRole.MANAGER.value:
        return True
    
    # 任务负责人可以编辑自己负责的任务
    if task.assignee_id and current_user.id == task.assignee_id:
        return True
    
    # 任务创建者可以编辑自己创建的任务
    if current_user.id == task.created_by:
        return True
    
    # 其他情况无权限
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="您没有权限编辑此任务"
    )


def check_task_view_permission(
    current_user: User, 
    task: Task, 
    db: Session
) -> bool:
    """
    检查用户是否有权限查看任务
    
    Args:
        current_user: 当前用户
        task: 要查看的任务
        db: 数据库会话
        
    Returns:
        bool: 是否有权限查看
        
    Raises:
        HTTPException: 权限不足时抛出异常
    """
    # 所有用户都可以查看任务（基本权限）
    # 这里可以添加更复杂的权限逻辑
    return True


def check_task_delete_permission(
    current_user: User, 
    task: Task, 
    db: Session
) -> bool:
    """
    检查用户是否有权限删除任务
    
    Args:
        current_user: 当前用户
        task: 要删除的任务
        db: 数据库会话
        
    Returns:
        bool: 是否有权限删除
        
    Raises:
        HTTPException: 权限不足时抛出异常
    """
    # 管理员可以删除所有任务
    if current_user.role == UserRole.ADMIN.value:
        return True
    
    # 项目经理可以删除所有任务
    if current_user.role == UserRole.MANAGER.value:
        return True
    
    # 任务创建者可以删除自己创建的任务
    if current_user.id == task.created_by:
        return True
    
    # 其他情况无权限
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="您没有权限删除此任务"
    )


def is_manager_or_admin(current_user: User) -> bool:
    """
    检查用户是否为管理员或项目经理
    
    Args:
        current_user: 当前用户
        
    Returns:
        bool: 是否为管理员或项目经理
    """
    return current_user.role in [UserRole.ADMIN.value, UserRole.MANAGER.value]
