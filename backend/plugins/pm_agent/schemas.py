"""
项目管理 Agent Pydantic 模式
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from models import TaskPriority, TaskStatus, UserRole, UserStatus
import uuid


class TaskBase(BaseModel):
    """任务基础模式"""
    title: str = Field(..., min_length=1, max_length=100, description="任务标题")
    description: Optional[str] = Field(None, max_length=500, description="任务描述")
    assignee_id: Optional[uuid.UUID] = Field(None, description="负责人ID")
    due_date: datetime = Field(..., description="截止日期")
    priority: str = Field("medium", description="任务优先级")


class TaskCreate(TaskBase):
    """创建任务模式"""
    pass


class TaskUpdate(BaseModel):
    """更新任务模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="任务标题")
    description: Optional[str] = Field(None, max_length=500, description="任务描述")
    assignee_id: Optional[uuid.UUID] = Field(None, description="负责人ID")
    due_date: Optional[datetime] = Field(None, description="截止日期")
    priority: Optional[str] = Field(None, description="任务优先级")
    status: Optional[str] = Field(None, description="任务状态")


class TaskResponse(TaskBase):
    """任务响应模式"""
    id: uuid.UUID
    status: str
    created_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """任务列表响应模式"""
    tasks: List[TaskResponse]
    total: int
    skip: int
    limit: int


class TaskHistoryResponse(BaseModel):
    """任务历史记录响应模式"""
    id: uuid.UUID
    task_id: uuid.UUID
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    changed_by: uuid.UUID
    changed_at: datetime
    
    class Config:
        from_attributes = True


class TaskStatusUpdate(BaseModel):
    """任务状态更新模式"""
    status: str = Field(..., description="任务状态")
    reason: Optional[str] = Field(None, max_length=500, description="状态变更原因")


class UserBase(BaseModel):
    """用户基础模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., max_length=100, description="邮箱")
    role: str = Field("member", description="用户角色")
    status: str = Field("active", description="用户状态")


class UserCreate(UserBase):
    """创建用户模式"""
    password: str = Field(..., min_length=6, description="密码")


class UserUpdate(BaseModel):
    """更新用户模式"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, max_length=100, description="邮箱")
    password: Optional[str] = Field(None, min_length=6, description="密码")
    role: Optional[str] = Field(None, description="用户角色")
    status: Optional[str] = Field(None, description="用户状态")


class UserResponse(UserBase):
    """用户响应模式"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """用户列表响应模式"""
    users: list[UserResponse]
    total: int
    skip: int
    limit: int


class HealthResponse(BaseModel):
    """健康检查响应模式"""
    status: str
    service: str
    database: dict


# ---------- Auth Schemas ----------

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(UserResponse):
    pass
