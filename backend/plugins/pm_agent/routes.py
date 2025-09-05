"""
项目管理 Agent 路由模块
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db, check_db_health
from models import User, Task, TaskPriority, TaskStatus, TaskHistory
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, TaskHistoryResponse, TaskStatusUpdate
from security import get_current_user
from permissions import check_task_edit_permission, check_task_view_permission, is_manager_or_admin
from task_history_service import record_task_update, get_task_history
from typing import List, Optional
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查端点"""
    db_health = await check_db_health()
    return {
        "status": "ok",
        "service": "项目管理Agent",
        "database": db_health
    }


@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    status: Optional[str] = None,
    assignee_id: Optional[uuid.UUID] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务列表"""
    try:
        query = db.query(Task).filter(Task.deleted_at.is_(None))
        
        # 过滤条件
        if status:
            query = query.filter(Task.status == status)
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        if priority:
            query = query.filter(Task.priority == priority)
        if search:
            query = query.filter(
                (Task.title.ilike(f"%{search}%")) |
                (Task.description.ilike(f"%{search}%"))
            )
        
        # 获取总数
        total = query.count()
        
        # 分页
        tasks = query.offset(offset).limit(limit).all()
        
        return TaskListResponse(
            tasks=tasks,
            total=total,
            skip=offset,
            limit=limit
        )
    except Exception as e:
        logger.error(f"获取任务列表时发生错误: {e}")
        return TaskListResponse(tasks=[], total=0, skip=offset, limit=limit)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取特定任务详情"""
    try:
        db_task = db.query(Task).filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
        
        # 检查查看权限
        check_task_view_permission(current_user, db_task, db)
        
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取任务详情时发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取任务详情失败"
        )


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新任务"""
    try:
        # 验证负责人是否存在
        if task.assignee_id:
            assignee = db.query(User).filter(User.id == task.assignee_id).first()
            if not assignee:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="指定的负责人不存在"
                )
        
        # 验证优先级
        if task.priority not in [p.value for p in TaskPriority]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的优先级: {task.priority}. 有效选项: {[p.value for p in TaskPriority]}"
            )
        
        # 创建任务
        db_task = Task(
            title=task.title,
            description=task.description,
            assignee_id=task.assignee_id,
            due_date=task.due_date,
            priority=task.priority,
            status=TaskStatus.PENDING.value,
            created_by=current_user.id
        )
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        logger.info(f"用户 {current_user.username} 创建了任务: {db_task.title}")
        return db_task
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"数据库完整性错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="任务创建失败，数据冲突"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"创建任务时发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建任务失败"
        )


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: uuid.UUID,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务信息"""
    try:
        db_task = db.query(Task).filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
        
        # 检查编辑权限
        check_task_edit_permission(current_user, db_task, db)
        
        # 验证负责人是否存在
        if task_update.assignee_id:
            assignee = db.query(User).filter(User.id == task_update.assignee_id).first()
            if not assignee:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="指定的负责人不存在"
                )
        
        # 验证优先级
        if task_update.priority and task_update.priority not in [p.value for p in TaskPriority]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的优先级: {task_update.priority}. 有效选项: {[p.value for p in TaskPriority]}"
            )
        
        # 验证状态
        if task_update.status and task_update.status not in [s.value for s in TaskStatus]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的状态: {task_update.status}. 有效选项: {[s.value for s in TaskStatus]}"
            )
        
        # 记录更新前的数据
        update_data = task_update.model_dump(exclude_unset=True)
        
        # 更新字段
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        # 记录历史变更
        record_task_update(db, db_task, update_data, current_user)
        
        logger.info(f"用户 {current_user.username} 更新了任务: {db_task.title}")
        return db_task
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"数据库完整性错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="任务更新失败，数据冲突"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"更新任务时发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新任务失败"
        )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除任务（软删除）"""
    try:
        db_task = db.query(Task).filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
        
        # 软删除：设置deleted_at字段
        from datetime import datetime
        db_task.deleted_at = datetime.utcnow()
        
        db.add(db_task)
        db.commit()
        
        logger.info(f"用户 {current_user.username} 删除了任务: {db_task.title}")
        return {"message": "任务删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除任务时发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除任务失败"
        )


@router.put("/tasks/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: uuid.UUID,
    status_update: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新任务状态"""
    try:
        db_task = db.query(Task).filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
        
        # 检查编辑权限
        check_task_edit_permission(current_user, db_task, db)
        
        # 验证状态
        if status_update.status not in [s.value for s in TaskStatus]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的状态: {status_update.status}. 有效选项: {[s.value for s in TaskStatus]}"
            )
        
        # 状态转换验证
        old_status = db_task.status
        new_status = status_update.status
        
        # 定义允许的状态转换
        allowed_transitions = {
            TaskStatus.PENDING.value: [TaskStatus.IN_PROGRESS.value, TaskStatus.BLOCKED.value, TaskStatus.OVERDUE.value],
            TaskStatus.IN_PROGRESS.value: [TaskStatus.COMPLETED.value, TaskStatus.BLOCKED.value, TaskStatus.OVERDUE.value],
            TaskStatus.BLOCKED.value: [TaskStatus.PENDING.value, TaskStatus.IN_PROGRESS.value, TaskStatus.OVERDUE.value],
            TaskStatus.OVERDUE.value: [TaskStatus.IN_PROGRESS.value, TaskStatus.COMPLETED.value, TaskStatus.BLOCKED.value],
            TaskStatus.COMPLETED.value: [TaskStatus.IN_PROGRESS.value, TaskStatus.BLOCKED.value]  # 已完成的任务可以重新开始
        }
        
        if new_status not in allowed_transitions.get(old_status, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不允许从状态 '{old_status}' 转换到 '{new_status}'"
            )
        
        # 更新状态
        db_task.status = new_status
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        # 记录状态变更历史
        record_task_update(db, db_task, {"status": new_status}, current_user)
        
        logger.info(f"用户 {current_user.username} 将任务 {db_task.title} 状态从 {old_status} 更新为 {new_status}")
        return db_task
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新任务状态时发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新任务状态失败"
        )


@router.get("/tasks/{task_id}/history", response_model=List[TaskHistoryResponse])
async def get_task_history_endpoint(
    task_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取任务历史记录"""
    try:
        # 检查任务是否存在
        db_task = db.query(Task).filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
        
        # 检查查看权限
        check_task_view_permission(current_user, db_task, db)
        
        # 获取历史记录
        history_records = get_task_history(db, str(task_id), limit, offset)
        
        return history_records
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取任务历史记录时发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取任务历史记录失败"
        )
