"""
项目管理 Agent 路由模块
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, check_db_health
from models import User, Task
from schemas import TaskCreate, TaskUpdate, TaskResponse
from typing import List

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


@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    status: str = None,
    assignee_id: str = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """获取任务列表"""
    try:
        query = db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if assignee_id:
            query = query.filter(Task.assignee_id == assignee_id)
        
        tasks = query.offset(offset).limit(limit).all()
        return tasks
    except Exception as e:
        # 返回空列表以保证服务可用性（日志记录留待接入logger）
        return []


@router.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """创建新任务"""
    try:
        db_task = Task(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建任务失败: {str(e)}")


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """更新任务信息"""
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        for field, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, field, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新任务失败: {str(e)}")


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """删除任务（软删除）"""
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        # 软删除：设置deleted_at字段
        from datetime import datetime
        db_task.deleted_at = datetime.utcnow()
        
        db.commit()
        return {"message": "任务删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除任务失败: {str(e)}")
