"""
项目管理 Agent 数据模型
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    GUEST = "guest"


class UserStatus(str, enum.Enum):
    """用户状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class TaskPriority(str, enum.Enum):
    """任务优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, enum.Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    OVERDUE = "overdue"


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default=UserRole.MEMBER.value)
    status = Column(String(20), nullable=False, default=UserStatus.ACTIVE.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    created_tasks = relationship("Task", foreign_keys="Task.created_by", back_populates="creator")
    assigned_tasks = relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee")


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=False)
    priority = Column(String(10), nullable=False, default=TaskPriority.MEDIUM.value)
    status = Column(String(20), nullable=False, default=TaskStatus.PENDING.value)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关系
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="assigned_tasks")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_tasks")
    history = relationship("TaskHistory", back_populates="task")


class TaskHistory(Base):
    """任务历史记录模型"""
    __tablename__ = "task_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    field_name = Column(String(50), nullable=False)
    old_value = Column(Text)
    new_value = Column(Text)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    task = relationship("Task", back_populates="history")
    changer = relationship("User", foreign_keys=[changed_by])


class TaskDeletionLog(Base):
    """任务删除日志模型"""
    __tablename__ = "task_deletion_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    deleted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    deletion_reason = Column(Text, nullable=True)
    deleted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    task = relationship("Task")
    deleter = relationship("User", foreign_keys=[deleted_by])
