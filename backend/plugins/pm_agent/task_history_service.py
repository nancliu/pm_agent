"""
任务历史记录服务
"""

from sqlalchemy.orm import Session
from models import Task, TaskHistory, User
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def create_task_history_entry(
    db: Session,
    task: Task,
    field_name: str,
    old_value: Optional[str],
    new_value: Optional[str],
    changed_by: User
) -> TaskHistory:
    """
    创建任务历史记录条目
    
    Args:
        db: 数据库会话
        task: 任务对象
        field_name: 变更字段名
        old_value: 旧值
        new_value: 新值
        changed_by: 变更用户
        
    Returns:
        TaskHistory: 创建的历史记录条目
    """
    history_entry = TaskHistory(
        task_id=task.id,
        field_name=field_name,
        old_value=old_value,
        new_value=new_value,
        changed_by=changed_by.id
    )
    
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    
    logger.info(f"用户 {changed_by.username} 修改了任务 {task.title} 的 {field_name} 字段")
    
    return history_entry


def record_task_update(
    db: Session,
    task: Task,
    update_data: Dict[str, Any],
    changed_by: User
) -> None:
    """
    记录任务更新历史
    
    Args:
        db: 数据库会话
        task: 任务对象
        update_data: 更新数据字典
        changed_by: 变更用户
    """
    # 记录每个变更的字段
    for field_name, new_value in update_data.items():
        if field_name in ['id', 'created_at', 'updated_at', 'deleted_at']:
            continue  # 跳过系统字段
            
        old_value = getattr(task, field_name, None)
        
        # 转换值为字符串进行比较
        if old_value is not None:
            old_value_str = str(old_value)
        else:
            old_value_str = None
            
        if new_value is not None:
            new_value_str = str(new_value)
        else:
            new_value_str = None
        
        # 只有当值真正发生变化时才记录
        if old_value_str != new_value_str:
            create_task_history_entry(
                db=db,
                task=task,
                field_name=field_name,
                old_value=old_value_str,
                new_value=new_value_str,
                changed_by=changed_by
            )


def get_task_history(
    db: Session,
    task_id: str,
    limit: int = 50,
    offset: int = 0
) -> list[TaskHistory]:
    """
    获取任务历史记录
    
    Args:
        db: 数据库会话
        task_id: 任务ID
        limit: 限制数量
        offset: 偏移量
        
    Returns:
        list[TaskHistory]: 历史记录列表
    """
    return db.query(TaskHistory)\
        .filter(TaskHistory.task_id == task_id)\
        .order_by(TaskHistory.changed_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()
