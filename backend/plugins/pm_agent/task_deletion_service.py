"""
任务删除服务
"""

from sqlalchemy.orm import Session
from models import Task, TaskDeletionLog, User
from typing import Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def create_deletion_log(
    db: Session,
    task: Task,
    deleted_by: User,
    deletion_reason: Optional[str] = None
) -> TaskDeletionLog:
    """
    创建任务删除日志
    
    Args:
        db: 数据库会话
        task: 被删除的任务
        deleted_by: 删除用户
        deletion_reason: 删除原因
        
    Returns:
        TaskDeletionLog: 删除日志条目
    """
    deletion_log = TaskDeletionLog(
        task_id=task.id,
        deleted_by=deleted_by.id,
        deletion_reason=deletion_reason
    )
    
    db.add(deletion_log)
    db.commit()
    db.refresh(deletion_log)
    
    logger.info(f"用户 {deleted_by.username} 删除了任务 {task.title}，原因: {deletion_reason or '无'}")
    
    return deletion_log


def soft_delete_task(
    db: Session,
    task: Task,
    deleted_by: User,
    deletion_reason: Optional[str] = None
) -> TaskDeletionLog:
    """
    软删除任务
    
    Args:
        db: 数据库会话
        task: 要删除的任务
        deleted_by: 删除用户
        deletion_reason: 删除原因
        
    Returns:
        TaskDeletionLog: 删除日志条目
    """
    # 设置删除时间
    task.deleted_at = datetime.utcnow()
    
    # 创建删除日志
    deletion_log = create_deletion_log(db, task, deleted_by, deletion_reason)
    
    # 保存任务
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return deletion_log


def restore_task(
    db: Session,
    task: Task,
    restored_by: User
) -> Task:
    """
    恢复任务
    
    Args:
        db: 数据库会话
        task: 要恢复的任务
        restored_by: 恢复用户
        
    Returns:
        Task: 恢复后的任务
    """
    # 清除删除时间
    task.deleted_at = None
    
    # 保存任务
    db.add(task)
    db.commit()
    db.refresh(task)
    
    logger.info(f"用户 {restored_by.username} 恢复了任务 {task.title}")
    
    return task


def get_deleted_tasks(
    db: Session,
    limit: int = 50,
    offset: int = 0
) -> list[Task]:
    """
    获取已删除的任务列表
    
    Args:
        db: 数据库会话
        limit: 限制数量
        offset: 偏移量
        
    Returns:
        list[Task]: 已删除任务列表
    """
    return db.query(Task)\
        .filter(Task.deleted_at.isnot(None))\
        .order_by(Task.deleted_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()


def get_deletion_logs(
    db: Session,
    task_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> list[TaskDeletionLog]:
    """
    获取删除日志
    
    Args:
        db: 数据库会话
        task_id: 任务ID（可选）
        limit: 限制数量
        offset: 偏移量
        
    Returns:
        list[TaskDeletionLog]: 删除日志列表
    """
    query = db.query(TaskDeletionLog)
    
    if task_id:
        query = query.filter(TaskDeletionLog.task_id == task_id)
    
    return query.order_by(TaskDeletionLog.deleted_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()
