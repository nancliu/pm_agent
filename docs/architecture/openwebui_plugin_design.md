# OpenWebUI 插件系统设计文档

## 插件架构概述

基于OpenWebUI原生插件系统，设计一个完整的项目管理Agent插件，实现任务管理、进度跟踪、到期提醒等核心功能。

## 插件目录结构

```
backend/plugins/pm_agent/
├── __init__.py                     # 插件初始化
├── main.py                         # 插件主入口
├── plugin.yaml                     # 插件配置文件
├── requirements.txt                 # 插件依赖
│
├── core/                           # 核心业务逻辑
│   ├── __init__.py
│   ├── agent.py                    # Agent核心类
│   ├── task_manager.py             # 任务管理器
│   ├── query_processor.py          # 查询处理器
│   ├── reminder_service.py         # 提醒服务
│   └── feishu_integration.py       # 飞书集成
│
├── tools/                          # 工具函数
│   ├── __init__.py
│   ├── task_tools.py               # 任务相关工具
│   ├── query_tools.py              # 查询相关工具
│   ├── reminder_tools.py           # 提醒相关工具
│   ├── export_tools.py             # 导出相关工具
│   └── user_tools.py               # 用户相关工具
│
├── utils/                          # 工具函数
│   ├── __init__.py
│   ├── nlp.py                      # 自然语言处理
│   ├── validators.py               # 数据验证
│   ├── helpers.py                  # 辅助函数
│   ├── database.py                 # 数据库操作
│   └── config.py                   # 配置管理
│
├── models/                         # 数据模型
│   ├── __init__.py
│   ├── task.py                     # 任务模型
│   ├── user.py                     # 用户模型
│   └── base.py                     # 基础模型
│
├── services/                       # 业务服务
│   ├── __init__.py
│   ├── task_service.py             # 任务服务
│   ├── user_service.py             # 用户服务
│   ├── feishu_service.py           # 飞书服务
│   ├── export_service.py           # 导出服务
│   └── backup_service.py           # 备份服务
│
├── scheduler/                      # 定时任务
│   ├── __init__.py
│   ├── reminder_scheduler.py       # 提醒调度器
│   └── backup_scheduler.py         # 备份调度器
│
└── tests/                          # 测试代码
    ├── __init__.py
    ├── test_agent.py
    ├── test_tasks.py
    ├── test_queries.py
    └── test_reminders.py
```

## 核心组件设计

### 1. 插件主入口 (main.py)

```python
"""
项目管理Agent插件主入口
"""
from openwebui import Plugin, PluginContext
from openwebui import function, webhook
from typing import Dict, Any, List, Optional
import logging

from .core.agent import ProjectManagementAgent
from .core.task_manager import TaskManager
from .core.query_processor import QueryProcessor
from .core.reminder_service import ReminderService
from .utils.config import PluginConfig
from .utils.database import DatabaseManager

logger = logging.getLogger(__name__)

class PMAgentPlugin(Plugin):
    """项目管理Agent插件"""
    
    def __init__(self):
        super().__init__()
        self.name = "项目管理Agent"
        self.version = "1.0.0"
        self.description = "科研项目管理智能助手，支持任务管理、进度跟踪、到期提醒"
        
        # 初始化核心组件
        self.config = PluginConfig()
        self.db = DatabaseManager()
        self.agent = ProjectManagementAgent(self.db)
        self.task_manager = TaskManager(self.db)
        self.query_processor = QueryProcessor(self.db)
        self.reminder_service = ReminderService(self.db)
        
        # 启动定时任务
        self.reminder_service.start_scheduler()
        
        logger.info("项目管理Agent插件初始化完成")
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """获取插件信息"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": "PM Agent Team",
            "functions": [
                "create_task",
                "update_task", 
                "delete_task",
                "query_tasks",
                "get_task_details",
                "export_tasks",
                "generate_report"
            ]
        }
    
    # ==================== 任务管理工具函数 ====================
    
    @function
    def create_task(
        self,
        title: str,
        assignee: str,
        due_date: str,
        description: str = "",
        priority: str = "中",
        start_date: str = None
    ) -> Dict[str, Any]:
        """
        创建新任务
        
        Args:
            title: 任务标题 (必填，最大200字符)
            assignee: 负责人 (必填，用户名或邮箱)
            due_date: 截止日期 (必填，YYYY-MM-DD格式)
            description: 任务描述 (可选，支持Markdown)
            priority: 优先级 (可选，高/中/低，默认中)
            start_date: 开始日期 (可选，YYYY-MM-DD格式)
        
        Returns:
            创建结果信息，包含任务ID和详细信息
        """
        try:
            result = self.task_manager.create_task({
                "title": title,
                "assignee": assignee,
                "due_date": due_date,
                "description": description,
                "priority": priority,
                "start_date": start_date
            })
            
            return {
                "success": True,
                "message": f"任务 '{title}' 创建成功",
                "task_id": result["task_id"],
                "data": result
            }
        except Exception as e:
            logger.error(f"创建任务失败: {e}")
            return {
                "success": False,
                "message": f"创建任务失败: {str(e)}"
            }
    
    @function
    def update_task(
        self,
        task_id: int,
        title: str = None,
        assignee: str = None,
        due_date: str = None,
        description: str = None,
        priority: str = None,
        status: str = None
    ) -> Dict[str, Any]:
        """
        更新任务信息
        
        Args:
            task_id: 任务ID
            title: 任务标题
            assignee: 负责人
            due_date: 截止日期
            description: 任务描述
            priority: 优先级
            status: 任务状态
        
        Returns:
            更新结果信息
        """
        try:
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if assignee is not None:
                update_data["assignee"] = assignee
            if due_date is not None:
                update_data["due_date"] = due_date
            if description is not None:
                update_data["description"] = description
            if priority is not None:
                update_data["priority"] = priority
            if status is not None:
                update_data["status"] = status
            
            result = self.task_manager.update_task(task_id, update_data)
            
            return {
                "success": True,
                "message": f"任务 {task_id} 更新成功",
                "data": result
            }
        except Exception as e:
            logger.error(f"更新任务失败: {e}")
            return {
                "success": False,
                "message": f"更新任务失败: {str(e)}"
            }
    
    @function
    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """
        删除任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            删除结果信息
        """
        try:
            result = self.task_manager.delete_task(task_id)
            
            return {
                "success": True,
                "message": f"任务 {task_id} 删除成功",
                "data": result
            }
        except Exception as e:
            logger.error(f"删除任务失败: {e}")
            return {
                "success": False,
                "message": f"删除任务失败: {str(e)}"
            }
    
    # ==================== 查询工具函数 ====================
    
    @function
    def query_tasks(
        self,
        assignee: str = None,
        status: str = None,
        priority: str = None,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        查询任务列表
        
        Args:
            assignee: 负责人
            status: 任务状态
            priority: 优先级
            limit: 返回数量限制
            offset: 偏移量
        
        Returns:
            任务列表
        """
        try:
            filters = {}
            if assignee:
                filters["assignee"] = assignee
            if status:
                filters["status"] = status
            if priority:
                filters["priority"] = priority
            
            result = self.query_processor.get_tasks(filters, limit, offset)
            
            return {
                "success": True,
                "message": f"查询到 {len(result['tasks'])} 个任务",
                "data": result
            }
        except Exception as e:
            logger.error(f"查询任务失败: {e}")
            return {
                "success": False,
                "message": f"查询任务失败: {str(e)}"
            }
    
    @function
    def get_task_details(self, task_id: int) -> Dict[str, Any]:
        """
        获取任务详细信息
        
        Args:
            task_id: 任务ID
        
        Returns:
            任务详细信息
        """
        try:
            result = self.query_processor.get_task_details(task_id)
            
            return {
                "success": True,
                "message": "获取任务详情成功",
                "data": result
            }
        except Exception as e:
            logger.error(f"获取任务详情失败: {e}")
            return {
                "success": False,
                "message": f"获取任务详情失败: {str(e)}"
            }
    
    # ==================== 导出工具函数 ====================
    
    @function
    def export_tasks(
        self,
        format: str = "excel",
        assignee: str = None,
        status: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, Any]:
        """
        导出任务数据
        
        Args:
            format: 导出格式 (excel/pdf)
            assignee: 负责人筛选
            status: 状态筛选
            start_date: 开始日期筛选
            end_date: 结束日期筛选
        
        Returns:
            导出结果信息
        """
        try:
            filters = {}
            if assignee:
                filters["assignee"] = assignee
            if status:
                filters["status"] = status
            if start_date:
                filters["start_date"] = start_date
            if end_date:
                filters["end_date"] = end_date
            
            result = self.task_manager.export_tasks(format, filters)
            
            return {
                "success": True,
                "message": f"任务数据导出成功 ({format.upper()})",
                "data": result
            }
        except Exception as e:
            logger.error(f"导出任务失败: {e}")
            return {
                "success": False,
                "message": f"导出任务失败: {str(e)}"
            }
    
    @function
    def generate_report(
        self,
        report_type: str = "progress",
        project_id: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, Any]:
        """
        生成项目报告
        
        Args:
            report_type: 报告类型 (progress/summary/detailed)
            project_id: 项目ID
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            报告生成结果
        """
        try:
            result = self.task_manager.generate_report(
                report_type, project_id, start_date, end_date
            )
            
            return {
                "success": True,
                "message": f"{report_type} 报告生成成功",
                "data": result
            }
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return {
                "success": False,
                "message": f"生成报告失败: {str(e)}"
            }
    
    # ==================== 飞书集成 ====================
    
    @webhook("/feishu/webhook")
    def handle_feishu_message(self, request) -> Dict[str, Any]:
        """
        处理飞书机器人消息
        
        Args:
            request: 飞书Webhook请求
        
        Returns:
            响应消息
        """
        try:
            message_data = request.json
            user_id = message_data.get("sender", {}).get("sender_id", {}).get("user_id")
            text = message_data.get("text", "")
            
            # 使用Agent处理自然语言消息
            response = self.agent.process_natural_language(text, user_id)
            
            return {
                "msg_type": "text",
                "content": {
                    "text": response
                }
            }
        except Exception as e:
            logger.error(f"处理飞书消息失败: {e}")
            return {
                "msg_type": "text",
                "content": {
                    "text": f"处理消息时发生错误: {str(e)}"
                }
            }
    
    # ==================== 自然语言处理 ====================
    
    @function
    def process_natural_language(self, text: str, user_id: str = None) -> Dict[str, Any]:
        """
        处理自然语言输入
        
        Args:
            text: 用户输入的自然语言文本
            user_id: 用户ID
        
        Returns:
            处理结果
        """
        try:
            result = self.agent.process_natural_language(text, user_id)
            
            return {
                "success": True,
                "message": "自然语言处理成功",
                "data": result
            }
        except Exception as e:
            logger.error(f"自然语言处理失败: {e}")
            return {
                "success": False,
                "message": f"自然语言处理失败: {str(e)}"
            }
    
    # ==================== 用户管理工具函数 ====================
    
    @function
    def create_user(
        self,
        username: str,
        full_name: str,
        email: str = None,
        role: str = "member",
        feishu_user_id: str = None
    ) -> Dict[str, Any]:
        """
        创建新用户
        
        Args:
            username: 用户名 (必填，唯一标识)
            full_name: 全名 (必填)
            email: 邮箱 (可选，用于通知)
            role: 角色 (可选，admin/manager/member，默认member)
            feishu_user_id: 飞书用户ID (可选，用于飞书集成)
        
        Returns:
            创建结果信息
        """
        try:
            result = self.task_manager.create_user({
                "username": username,
                "full_name": full_name,
                "email": email,
                "role": role,
                "feishu_user_id": feishu_user_id
            })
            
            return {
                "success": True,
                "message": f"用户 '{username}' 创建成功",
                "data": result
            }
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            return {
                "success": False,
                "message": f"创建用户失败: {str(e)}"
            }
    
    @function
    def get_users(
        self,
        role: str = None,
        is_active: bool = True,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        获取用户列表
        
        Args:
            role: 角色筛选 (可选)
            is_active: 是否激活 (可选，默认true)
            limit: 返回数量限制 (可选，默认50)
            offset: 偏移量 (可选，默认0)
        
        Returns:
            用户列表
        """
        try:
            filters = {}
            if role:
                filters["role"] = role
            if is_active is not None:
                filters["is_active"] = is_active
            
            result = self.task_manager.get_users(filters, limit, offset)
            
            return {
                "success": True,
                "message": f"查询到 {len(result['users'])} 个用户",
                "data": result
            }
        except Exception as e:
            logger.error(f"查询用户失败: {e}")
            return {
                "success": False,
                "message": f"查询用户失败: {str(e)}"
            }
    
    # ==================== 系统管理 ====================
    
    @function
    def get_system_status(self) -> Dict[str, Any]:
        """
        获取系统状态
        
        Returns:
            系统状态信息
        """
        try:
            status = {
                "database": self.db.check_connection(),
                "scheduler": self.reminder_service.get_status(),
                "feishu": self.agent.feishu_service.check_connection(),
                "tasks_count": self.task_manager.get_tasks_count(),
                "users_count": self.task_manager.get_users_count()
            }
            
            return {
                "success": True,
                "message": "系统状态获取成功",
                "data": status
            }
        except Exception as e:
            logger.error(f"获取系统状态失败: {e}")
            return {
                "success": False,
                "message": f"获取系统状态失败: {str(e)}"
            }
    
    def cleanup(self):
        """插件清理"""
        try:
            self.reminder_service.stop_scheduler()
            self.db.close_connection()
            logger.info("项目管理Agent插件清理完成")
        except Exception as e:
            logger.error(f"插件清理失败: {e}")

# 插件实例
plugin = PMAgentPlugin()
```

### 2. 插件配置文件 (plugin.yaml)

```yaml
name: "pm-agent"
version: "1.0.0"
description: "科研项目管理智能助手"
author: "PM Agent Team"
license: "MIT"

# 插件依赖
dependencies:
  - "fastapi>=0.100.0"
  - "sqlalchemy>=2.0.0"
  - "psycopg2-binary>=2.9.0"
  - "apscheduler>=3.10.0"
  - "feishu-sdk>=1.0.0"
  - "openpyxl>=3.1.0"
  - "reportlab>=4.0.0"
  - "python-dateutil>=2.8.0"
  - "pydantic>=2.0.0"
  - "pyjwt>=2.8.0"
  - "bcrypt>=4.0.0"
  - "redis>=4.5.0"
  - "pgvector>=0.2.0"

# 插件配置
config:
  database:
    url: "${DATABASE_URL}"
    pool_size: 10
    max_overflow: 20
    echo: false
  
  feishu:
    app_id: "${FEISHU_APP_ID}"
    app_secret: "${FEISHU_APP_SECRET}"
    webhook_url: "${FEISHU_WEBHOOK_URL}"
    timeout: 30
  
  scheduler:
    timezone: "Asia/Shanghai"
    reminder_time: "09:00"
    reminder_days: 3
    overdue_check_time: "18:00"
  
  export:
    max_file_size: "10MB"
    allowed_formats: ["excel", "pdf", "csv"]
    storage_path: "/app/data/exports"
    cleanup_days: 7
  
  auth:
    jwt_secret: "${JWT_SECRET}"
    jwt_expire_hours: 24
    password_min_length: 8
  
  cache:
    redis_url: "${REDIS_URL}"
    default_ttl: 3600
  
  performance:
    max_tasks_per_page: 20
    max_users_per_page: 50
    query_timeout: 5

# 插件入口点
entry_point: "main:plugin"

# 插件标签
tags:
  - "project-management"
  - "task-management"
  - "feishu-integration"
  - "ai-agent"

# 插件权限
permissions:
  - "database:read"
  - "database:write"
  - "file:export"
  - "webhook:receive"
  - "scheduler:manage"

# 插件健康检查
health_check:
  endpoint: "/health"
  interval: 30
  timeout: 10

# 插件日志配置
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "/app/logs/pm_agent.log"
  max_size: "10MB"
  backup_count: 5
```

### 3. Agent核心类 (core/agent.py)

```python
"""
项目管理Agent核心类
"""
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta

from ..utils.nlp import NLPProcessor
from ..services.feishu_service import FeishuService
from ..core.task_manager import TaskManager
from ..core.query_processor import QueryProcessor

logger = logging.getLogger(__name__)

class ProjectManagementAgent:
    """项目管理Agent核心类"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.nlp_processor = NLPProcessor()
        self.feishu_service = FeishuService()
        self.task_manager = TaskManager(db_manager)
        self.query_processor = QueryProcessor(db_manager)
        
        # 初始化自然语言处理规则
        self._init_nlp_rules()
    
    def _init_nlp_rules(self):
        """初始化自然语言处理规则"""
        self.nlp_rules = {
            "create_task": [
                r"创建任务[：:]\s*(.+?)\s*负责[，,]\s*(.+?)[，,]\s*(.+?)\s*截止",
                r"新建任务[：:]\s*(.+?)\s*负责[，,]\s*(.+?)[，,]\s*(.+?)\s*截止",
                r"添加任务[：:]\s*(.+?)\s*负责[，,]\s*(.+?)[，,]\s*(.+?)\s*截止"
            ],
            "query_tasks": [
                r"查询(.+?)的任务",
                r"查看(.+?)的任务",
                r"(.+?)有什么任务",
                r"我的任务",
                r"所有任务"
            ],
            "update_task": [
                r"更新任务(.+?)的状态为(.+)",
                r"修改任务(.+?)的状态为(.+)",
                r"任务(.+?)完成",
                r"任务(.+?)延期"
            ]
        }
    
    def process_natural_language(self, text: str, user_id: str = None) -> str:
        """
        处理自然语言输入
        
        Args:
            text: 用户输入的自然语言文本
            user_id: 用户ID
        
        Returns:
            处理结果文本
        """
        try:
            # 意图识别
            intent = self._identify_intent(text)
            
            if intent == "create_task":
                return self._handle_create_task(text, user_id)
            elif intent == "query_tasks":
                return self._handle_query_tasks(text, user_id)
            elif intent == "update_task":
                return self._handle_update_task(text, user_id)
            else:
                return self._handle_unknown_intent(text)
                
        except Exception as e:
            logger.error(f"自然语言处理失败: {e}")
            return f"处理您的请求时发生错误: {str(e)}"
    
    def _identify_intent(self, text: str) -> str:
        """识别用户意图"""
        text_lower = text.lower()
        
        # 检查任务创建意图
        for pattern in self.nlp_rules["create_task"]:
            if self.nlp_processor.match_pattern(text, pattern):
                return "create_task"
        
        # 检查任务查询意图
        for pattern in self.nlp_rules["query_tasks"]:
            if self.nlp_processor.match_pattern(text, pattern):
                return "query_tasks"
        
        # 检查任务更新意图
        for pattern in self.nlp_rules["update_task"]:
            if self.nlp_processor.match_pattern(text, pattern):
                return "update_task"
        
        return "unknown"
    
    def _handle_create_task(self, text: str, user_id: str = None) -> str:
        """处理任务创建请求"""
        try:
            # 解析任务信息
            task_info = self.nlp_processor.parse_task_creation(text)
            
            if not task_info:
                return "抱歉，我无法理解您的任务创建请求。请使用格式：创建任务：小王负责，完成前端页面优化，下周五截止"
            
            # 创建任务
            result = self.task_manager.create_task(task_info)
            
            if result["success"]:
                return f"✅ 任务创建成功！\n📋 任务：{task_info['title']}\n👤 负责人：{task_info['assignee']}\n📅 截止时间：{task_info['due_date']}\n🆔 任务ID：{result['task_id']}"
            else:
                return f"❌ 任务创建失败：{result['message']}"
                
        except Exception as e:
            logger.error(f"处理任务创建失败: {e}")
            return f"创建任务时发生错误：{str(e)}"
    
    def _handle_query_tasks(self, text: str, user_id: str = None) -> str:
        """处理任务查询请求"""
        try:
            # 解析查询条件
            query_info = self.nlp_processor.parse_query(text)
            
            # 执行查询
            result = self.query_processor.get_tasks(query_info)
            
            if not result["tasks"]:
                return "📭 没有找到符合条件的任务"
            
            # 格式化结果
            response = "📋 任务查询结果：\n\n"
            for task in result["tasks"]:
                status_emoji = self._get_status_emoji(task["status"])
                priority_emoji = self._get_priority_emoji(task["priority"])
                
                response += f"{status_emoji} **{task['title']}**\n"
                response += f"   👤 负责人：{task['assignee']}\n"
                response += f"   📅 截止时间：{task['due_date']}\n"
                response += f"   {priority_emoji} 优先级：{task['priority']}\n"
                response += f"   🆔 任务ID：{task['id']}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"处理任务查询失败: {e}")
            return f"查询任务时发生错误：{str(e)}"
    
    def _handle_update_task(self, text: str, user_id: str = None) -> str:
        """处理任务更新请求"""
        try:
            # 解析更新信息
            update_info = self.nlp_processor.parse_task_update(text)
            
            if not update_info:
                return "抱歉，我无法理解您的任务更新请求。请使用格式：更新任务123的状态为完成"
            
            # 更新任务
            result = self.task_manager.update_task(
                update_info["task_id"], 
                {"status": update_info["status"]}
            )
            
            if result["success"]:
                return f"✅ 任务 {update_info['task_id']} 状态已更新为：{update_info['status']}"
            else:
                return f"❌ 任务更新失败：{result['message']}"
                
        except Exception as e:
            logger.error(f"处理任务更新失败: {e}")
            return f"更新任务时发生错误：{str(e)}"
    
    def _handle_unknown_intent(self, text: str) -> str:
        """处理未知意图"""
        return """🤖 我是项目管理助手，可以帮助您：
        
📝 **创建任务**：创建任务：小王负责，完成前端页面优化，下周五截止
🔍 **查询任务**：查询小王的任务 / 我的任务 / 所有任务
📊 **更新任务**：更新任务123的状态为完成
📈 **生成报告**：生成进度报告
📤 **导出数据**：导出任务清单

请告诉我您需要什么帮助？"""
    
    def _get_status_emoji(self, status: str) -> str:
        """获取状态对应的表情符号"""
        status_emojis = {
            "未开始": "⏳",
            "进行中": "🔄",
            "完成": "✅",
            "延期": "⚠️"
        }
        return status_emojis.get(status, "❓")
    
    def _get_priority_emoji(self, priority: str) -> str:
        """获取优先级对应的表情符号"""
        priority_emojis = {
            "高": "🔴",
            "中": "🟡",
            "低": "🟢"
        }
        return priority_emojis.get(priority, "⚪")
    
    def send_reminder(self, user_id: str, message: str) -> bool:
        """发送提醒消息"""
        try:
            return self.feishu_service.send_message(user_id, message)
        except Exception as e:
            logger.error(f"发送提醒失败: {e}")
            return False
    
    def get_agent_status(self) -> Dict[str, Any]:
        """获取Agent状态"""
        return {
            "status": "running",
            "nlp_processor": self.nlp_processor.get_status(),
            "feishu_service": self.feishu_service.get_status(),
            "task_manager": self.task_manager.get_status(),
            "query_processor": self.query_processor.get_status()
        }
```

### 4. 自然语言处理工具 (utils/nlp.py)

```python
"""
自然语言处理工具
"""
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class NLPProcessor:
    """自然语言处理器"""
    
    def __init__(self):
        self.time_patterns = {
            r"今天": self._get_today,
            r"明天": self._get_tomorrow,
            r"后天": self._get_day_after_tomorrow,
            r"下周一": self._get_next_monday,
            r"下周二": self._get_next_tuesday,
            r"下周三": self._get_next_wednesday,
            r"下周四": self._get_next_thursday,
            r"下周五": self._get_next_friday,
            r"下周六": self._get_next_saturday,
            r"下周日": self._get_next_sunday,
            r"(\d+)天后": self._get_days_later,
            r"(\d+)周后": self._get_weeks_later,
            r"(\d+)月后": self._get_months_later
        }
    
    def match_pattern(self, text: str, pattern: str) -> bool:
        """检查文本是否匹配模式"""
        try:
            return bool(re.search(pattern, text))
        except Exception as e:
            logger.error(f"模式匹配失败: {e}")
            return False
    
    def parse_task_creation(self, text: str) -> Optional[Dict[str, Any]]:
        """
        解析任务创建语句
        
        示例: "创建任务：小王负责，完成前端页面优化，下周五截止"
        """
        try:
            # 任务创建模式
            patterns = [
                r"创建任务[：:]\s*(.+?)\s*负责[，,]\s*(.+?)[，,]\s*(.+?)\s*截止",
                r"新建任务[：:]\s*(.+?)\s*负责[，,]\s*(.+?)[，,]\s*(.+?)\s*截止",
                r"添加任务[：:]\s*(.+?)\s*负责[，,]\s*(.+?)[，,]\s*(.+?)\s*截止"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    assignee = match.group(1).strip()
                    description = match.group(2).strip()
                    due_date_text = match.group(3).strip()
                    
                    # 解析截止日期
                    due_date = self._parse_time_expression(due_date_text)
                    if not due_date:
                        continue
                    
                    return {
                        "title": description,
                        "description": description,
                        "assignee": assignee,
                        "due_date": due_date.strftime("%Y-%m-%d"),
                        "priority": "中",
                        "status": "未开始"
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"解析任务创建失败: {e}")
            return None
    
    def parse_query(self, text: str) -> Dict[str, Any]:
        """
        解析查询语句
        
        示例: "查询小王的任务", "我的任务", "所有任务"
        """
        try:
            query_info = {}
            
            # 个人任务查询
            if "我的任务" in text or "我的" in text:
                query_info["assignee"] = "current_user"  # 需要从上下文获取
            # 特定人员任务查询
            elif "查询" in text and "的任务" in text:
                match = re.search(r"查询(.+?)的任务", text)
                if match:
                    query_info["assignee"] = match.group(1).strip()
            # 所有任务查询
            elif "所有任务" in text or "全部任务" in text:
                pass  # 不添加筛选条件
            
            return query_info
            
        except Exception as e:
            logger.error(f"解析查询语句失败: {e}")
            return {}
    
    def parse_task_update(self, text: str) -> Optional[Dict[str, Any]]:
        """
        解析任务更新语句
        
        示例: "更新任务123的状态为完成", "任务123完成"
        """
        try:
            # 任务ID提取
            task_id_match = re.search(r"任务(\d+)", text)
            if not task_id_match:
                return None
            
            task_id = int(task_id_match.group(1))
            
            # 状态提取
            status = None
            if "完成" in text:
                status = "完成"
            elif "进行中" in text or "开始" in text:
                status = "进行中"
            elif "延期" in text:
                status = "延期"
            elif "未开始" in text:
                status = "未开始"
            
            if status:
                return {
                    "task_id": task_id,
                    "status": status
                }
            
            return None
            
        except Exception as e:
            logger.error(f"解析任务更新失败: {e}")
            return None
    
    def _parse_time_expression(self, time_text: str) -> Optional[datetime]:
        """解析时间表达式"""
        try:
            time_text = time_text.strip()
            
            # 检查预定义模式
            for pattern, handler in self.time_patterns.items():
                match = re.search(pattern, time_text)
                if match:
                    if match.groups():
                        return handler(int(match.group(1)))
                    else:
                        return handler()
            
            # 尝试解析标准日期格式
            try:
                return datetime.strptime(time_text, "%Y-%m-%d")
            except ValueError:
                pass
            
            try:
                return datetime.strptime(time_text, "%m-%d")
            except ValueError:
                pass
            
            return None
            
        except Exception as e:
            logger.error(f"解析时间表达式失败: {e}")
            return None
    
    def _get_today(self) -> datetime:
        """获取今天"""
        return datetime.now().date()
    
    def _get_tomorrow(self) -> datetime:
        """获取明天"""
        return (datetime.now() + timedelta(days=1)).date()
    
    def _get_day_after_tomorrow(self) -> datetime:
        """获取后天"""
        return (datetime.now() + timedelta(days=2)).date()
    
    def _get_next_monday(self) -> datetime:
        """获取下周一"""
        today = datetime.now()
        days_ahead = 0 - today.weekday()  # 周一为0
        if days_ahead <= 0:  # 如果今天是周一或之后
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).date()
    
    def _get_next_tuesday(self) -> datetime:
        """获取下周二"""
        today = datetime.now()
        days_ahead = 1 - today.weekday()  # 周二为1
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).date()
    
    def _get_next_wednesday(self) -> datetime:
        """获取下周三"""
        today = datetime.now()
        days_ahead = 2 - today.weekday()  # 周三为2
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).date()
    
    def _get_next_thursday(self) -> datetime:
        """获取下周四"""
        today = datetime.now()
        days_ahead = 3 - today.weekday()  # 周四为3
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).date()
    
    def _get_next_friday(self) -> datetime:
        """获取下周五"""
        today = datetime.now()
        days_ahead = 4 - today.weekday()  # 周五为4
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).date()
    
    def _get_next_saturday(self) -> datetime:
        """获取下周六"""
        today = datetime.now()
        days_ahead = 5 - today.weekday()  # 周六为5
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).date()
    
    def _get_next_sunday(self) -> datetime:
        """获取下周日"""
        today = datetime.now()
        days_ahead = 6 - today.weekday()  # 周日为6
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).date()
    
    def _get_days_later(self, days: int) -> datetime:
        """获取N天后"""
        return (datetime.now() + timedelta(days=days)).date()
    
    def _get_weeks_later(self, weeks: int) -> datetime:
        """获取N周后"""
        return (datetime.now() + timedelta(weeks=weeks)).date()
    
    def _get_months_later(self, months: int) -> datetime:
        """获取N月后"""
        today = datetime.now()
        year = today.year
        month = today.month + months
        while month > 12:
            month -= 12
            year += 1
        return datetime(year, month, today.day).date()
    
    def get_status(self) -> Dict[str, Any]:
        """获取处理器状态"""
        return {
            "status": "running",
            "time_patterns_count": len(self.time_patterns),
            "supported_formats": [
                "今天", "明天", "后天",
                "下周一", "下周二", "下周三", "下周四", "下周五", "下周六", "下周日",
                "N天后", "N周后", "N月后",
                "YYYY-MM-DD", "MM-DD"
            ]
        }
```

## 插件部署配置

### 1. 环境变量配置

```bash
# .env.local
# 数据库配置
DATABASE_URL=postgresql://pm_user:pm_password@localhost:5432/pm_agent

# 飞书配置
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_WEBHOOK_URL=https://your-domain.com/feishu/webhook

# 插件配置
PLUGIN_LOG_LEVEL=INFO
PLUGIN_LOG_FILE=/app/logs/pm_agent.log
PLUGIN_TIMEZONE=Asia/Shanghai
PLUGIN_REMINDER_TIME=09:00
PLUGIN_REMINDER_DAYS=3

# 导出配置
EXPORT_MAX_FILE_SIZE=10MB
EXPORT_STORAGE_PATH=/app/data/exports
EXPORT_ALLOWED_FORMATS=excel,pdf
```

### 2. Docker集成

```dockerfile
# Dockerfile.backend
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制插件代码
COPY backend/plugins/pm_agent /app/plugins/pm_agent
COPY backend/requirements.txt /app/requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要目录
RUN mkdir -p /app/logs /app/data/exports

# 设置环境变量
ENV PYTHONPATH=/app
ENV PLUGIN_PATH=/app/plugins

# 启动命令
CMD ["python", "-m", "openwebui", "--plugins", "pm_agent"]
```

这个OpenWebUI插件设计提供了完整的项目管理Agent功能，包括任务管理、自然语言处理、飞书集成、定时提醒等核心功能，同时保持了良好的可扩展性和维护性。
