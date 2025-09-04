# 项目管理 Agent MVP 技术架构文档

## 系统总体架构

### 架构概览

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web 前端       │    │   飞书机器人     │    │   定时任务      │
│  (React/Vue)    │    │  (Feishu Bot)   │    │  (APScheduler)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OpenWebUI + 插件系统                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   任务管理插件   │  │   查询插件      │  │   提醒插件      │ │
│  │  (Task Plugin)  │  │ (Query Plugin)  │  │(Reminder Plugin)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   导出插件      │  │   用户管理插件   │  │   认证插件      │ │
│  │ (Export Plugin) │  │ (User Plugin)   │  │ (Auth Plugin)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL 数据库                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   tasks 表      │  │   users 表      │  │   logs 表       │ │
│  │  (任务数据)      │  │  (用户数据)      │  │  (操作日志)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ task_history 表 │  │ export_records  │  │   sessions 表   │ │
│  │  (任务历史)      │  │    (导出记录)    │  │  (会话管理)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    知识库系统 (未来扩展)                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   PMBOK 知识库  │  │  PRINCE2 知识库 │  │   向量数据库    │ │
│  │  (项目管理指南)  │  │  (方法论指南)    │  │  (语义搜索)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 技术栈选型

### 后端技术栈
- **OpenWebUI**: 基于FastAPI的Web框架，支持插件机制
- **PostgreSQL 15+**: 关系型数据库，支持复杂查询和事务，支持pgvector扩展
- **SQLAlchemy 2.0+**: ORM框架，异步支持，简化数据库操作
- **APScheduler 3.10+**: 定时任务调度器，支持到期提醒和延期提醒
- **Pydantic 2.0+**: 数据验证和序列化，确保数据完整性
- **feishu-sdk 1.0+**: 飞书机器人SDK，支持自然语言交互
- **数据导出**: openpyxl (Excel), reportlab (PDF)
- **数据备份**: pg_dump, 定时备份脚本
- **JWT认证**: PyJWT，用户身份验证和权限管理
- **向量数据库**: pgvector (PostgreSQL扩展)，支持知识库语义搜索

### 前端技术栈
- **React 18+ / Vue.js 3+**: 前端框架，根据团队技术栈选择
- **Ant Design / Element UI**: UI组件库，提供丰富的组件
- **Axios**: HTTP客户端，API请求处理
- **图表库**: ECharts，支持甘特图、燃尽图、任务统计图表
- **导出库**: SheetJS (Excel), jsPDF (PDF)
- **状态管理**: Redux Toolkit / Pinia，应用状态管理
- **构建工具**: Vite / Webpack，前端构建和打包

### 飞书集成
- **飞书开放平台**: 机器人API
- **飞书SDK**: Python SDK for Feishu
- **Webhook**: 接收飞书消息

### 部署和运维
- **Docker**: 容器化部署
- **Docker Compose**: 多服务编排
- **Nginx**: 反向代理和负载均衡
- **Supervisor**: 进程管理

## 核心组件设计

### 1. OpenWebUI 插件系统

#### 1.1 任务管理插件 (Task Plugin)
```python
class TaskPlugin:
    def __init__(self):
        self.db = DatabaseManager()
        self.feishu_client = FeishuClient()
    
    def create_task(self, task_data):
        """创建任务"""
        pass
    
    def update_task(self, task_id, update_data):
        """更新任务"""
        pass
    
    def delete_task(self, task_id):
        """删除任务"""
        pass
    
    def get_tasks(self, filters=None):
        """获取任务列表"""
        pass
```

#### 1.2 查询插件 (Query Plugin)
```python
class QueryPlugin:
    def __init__(self):
        self.db = DatabaseManager()
        self.nlp_processor = NLPProcessor()
    
    def parse_query(self, query_text):
        """解析查询语句"""
        pass
    
    def search_tasks(self, search_criteria):
        """搜索任务"""
        pass
    
    def get_task_details(self, task_id):
        """获取任务详情"""
        pass
```

#### 1.3 提醒插件 (Reminder Plugin)
```python
class ReminderPlugin:
    def __init__(self):
        self.db = DatabaseManager()
        self.feishu_client = FeishuClient()
        self.scheduler = APScheduler()
    
    def check_due_tasks(self):
        """检查到期任务"""
        pass
    
    def send_reminder(self, user_id, message):
        """发送提醒"""
        pass
    
    def schedule_reminders(self):
        """调度提醒任务"""
        pass
```

#### 1.4 知识库插件 (Knowledge Plugin) - 未来扩展
```python
class KnowledgePlugin:
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.llm_client = LLMClient()
        self.pmbok_kb = PMBOKKnowledgeBase()
        self.prince2_kb = PRINCE2KnowledgeBase()
    
    def search_knowledge(self, query):
        """搜索项目管理知识"""
        pass
    
    def get_methodology_advice(self, task_context):
        """获取方法论建议"""
        pass
    
    def suggest_best_practices(self, project_phase):
        """建议最佳实践"""
        pass
```

### 2. 数据库设计

#### 2.1 核心表结构
```sql
-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    "fullName" VARCHAR(100) NOT NULL,
    feishu_user_id VARCHAR(50) UNIQUE,
    role VARCHAR(20) DEFAULT 'member' CHECK (role IN ('admin', 'manager', 'member')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- 任务表
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    assignee_id INTEGER REFERENCES users(id),
    "startDate" DATE,
    "dueDate" DATE NOT NULL,
    status VARCHAR(20) DEFAULT '未开始' CHECK (status IN ('未开始', '进行中', '完成', '延期')),
    priority VARCHAR(10) DEFAULT '中' CHECK (priority IN ('高', '中', '低')),
    "agentType" VARCHAR(20) DEFAULT '进度',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- 用户会话表
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

-- 操作日志表
CREATE TABLE operation_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    operation_type VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id INTEGER,
    operation_data JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- 任务历史表 (支持撤销和恢复)
CREATE TABLE task_history (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    operation_type VARCHAR(20) NOT NULL CHECK (operation_type IN ('CREATE', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT now()
);

-- 导出记录表
CREATE TABLE export_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    export_type VARCHAR(50) NOT NULL CHECK (export_type IN ('TASK_LIST', 'PROGRESS_REPORT', 'USER_REPORT')),
    file_path VARCHAR(500),
    file_size BIGINT,
    export_params JSONB,
    status VARCHAR(20) DEFAULT 'processing' CHECK (status IN ('processing', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT now(),
    completed_at TIMESTAMP
);

-- 提醒记录表
CREATE TABLE reminder_logs (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    user_id INTEGER REFERENCES users(id),
    reminder_type VARCHAR(20) NOT NULL CHECK (reminder_type IN ('due_soon', 'overdue', 'custom')),
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT now(),
    status VARCHAR(20) DEFAULT 'sent' CHECK (status IN ('sent', 'failed', 'pending'))
);

-- 知识库表 (未来扩展)
CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('PMBOK', 'PRINCE2', 'CUSTOM')),
    category VARCHAR(100),
    tags TEXT[],
    embedding VECTOR(1536), -- 向量嵌入 (使用pgvector)
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);
```

#### 2.2 索引设计
```sql
-- 用户表索引
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_feishu_id ON users (feishu_user_id);
CREATE INDEX idx_users_role ON users (role);
CREATE INDEX idx_users_is_active ON users (is_active);

-- 任务表索引
CREATE INDEX idx_tasks_assignee_id ON tasks (assignee_id);
CREATE INDEX idx_tasks_due_date ON tasks ("dueDate");
CREATE INDEX idx_tasks_status ON tasks (status);
CREATE INDEX idx_tasks_priority ON tasks (priority);
CREATE INDEX idx_tasks_created_at ON tasks (created_at);
CREATE INDEX idx_tasks_created_by ON tasks (created_by);
-- 复合索引用于常见查询
CREATE INDEX idx_tasks_assignee_status ON tasks (assignee_id, status);
CREATE INDEX idx_tasks_due_date_status ON tasks ("dueDate", status);

-- 用户会话表索引
CREATE INDEX idx_sessions_user_id ON user_sessions (user_id);
CREATE INDEX idx_sessions_token_hash ON user_sessions (token_hash);
CREATE INDEX idx_sessions_expires_at ON user_sessions (expires_at);

-- 操作日志表索引
CREATE INDEX idx_logs_user_id ON operation_logs (user_id);
CREATE INDEX idx_logs_operation_type ON operation_logs (operation_type);
CREATE INDEX idx_logs_resource_type ON operation_logs (resource_type);
CREATE INDEX idx_logs_created_at ON operation_logs (created_at);
-- 复合索引用于审计查询
CREATE INDEX idx_logs_user_operation ON operation_logs (user_id, operation_type);

-- 任务历史表索引
CREATE INDEX idx_task_history_task_id ON task_history (task_id);
CREATE INDEX idx_task_history_created_at ON task_history (created_at);
CREATE INDEX idx_task_history_operation_type ON task_history (operation_type);
CREATE INDEX idx_task_history_user_id ON task_history (user_id);

-- 导出记录表索引
CREATE INDEX idx_export_records_user_id ON export_records (user_id);
CREATE INDEX idx_export_records_export_type ON export_records (export_type);
CREATE INDEX idx_export_records_status ON export_records (status);
CREATE INDEX idx_export_records_created_at ON export_records (created_at);

-- 提醒记录表索引
CREATE INDEX idx_reminder_logs_task_id ON reminder_logs (task_id);
CREATE INDEX idx_reminder_logs_user_id ON reminder_logs (user_id);
CREATE INDEX idx_reminder_logs_reminder_type ON reminder_logs (reminder_type);
CREATE INDEX idx_reminder_logs_sent_at ON reminder_logs (sent_at);

-- 知识库表索引
CREATE INDEX idx_kb_source_type ON knowledge_base (source_type);
CREATE INDEX idx_kb_category ON knowledge_base (category);
CREATE INDEX idx_kb_tags ON knowledge_base USING GIN (tags);
-- 向量相似度搜索索引 (使用pgvector)
CREATE INDEX idx_kb_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops);
```

### 3. 飞书机器人集成

#### 3.1 消息处理流程
```
飞书消息 → Webhook → 消息解析 → 业务逻辑 → 数据库操作 → 响应消息
```

#### 3.2 自然语言处理
```python
class NLPProcessor:
    def parse_task_creation(self, text):
        """解析任务创建语句"""
        # 示例: "创建任务：小王负责，完成前端页面优化，下周五截止"
        pattern = r'创建任务[：:]\s*(.+?)\s*负责[，,]\s*(.+?)[，,]\s*(.+?)\s*截止'
        # 返回解析结果
        pass
    
    def parse_query(self, text):
        """解析查询语句"""
        # 示例: "查询小王的任务"
        # 示例: "查询我的任务"
        # 示例: "查询所有任务"
        pass
    
    def parse_time_expression(self, time_text):
        """解析时间表达式"""
        # 示例: "下周五" → 具体日期
        # 示例: "3天后" → 具体日期
        pass
```

### 4. 定时任务系统

#### 4.1 任务调度配置
```python
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

# 每天9:00检查到期任务
@scheduler.scheduled_job('cron', hour=9, minute=0)
def check_due_tasks():
    reminder_plugin = ReminderPlugin()
    reminder_plugin.check_due_tasks()

# 每天18:00检查延期任务
@scheduler.scheduled_job('cron', hour=18, minute=0)
def check_overdue_tasks():
    reminder_plugin = ReminderPlugin()
    reminder_plugin.check_overdue_tasks()
```

#### 4.2 提醒逻辑
```python
def check_due_tasks(self):
    """检查即将到期的任务"""
    # 查询3天内到期的任务
    due_tasks = self.db.query(
        "SELECT * FROM tasks WHERE due_date <= %s AND status != '完成'",
        (datetime.now() + timedelta(days=3),)
    )
    
    for task in due_tasks:
        self.send_reminder(task.assignee, f"任务即将到期: {task.title}")
```

## 数据流向设计

### 1. 任务创建流程
```
用户输入 → 数据验证 → 数据库存储 → 返回确认 → 日志记录
```

### 2. 任务查询流程
```
查询请求 → 权限验证 → 数据库查询 → 结果格式化 → 返回数据
```

### 3. 提醒流程
```
定时触发 → 数据库查询 → 消息生成 → 飞书发送 → 发送记录
```

## 安全设计

### 1. 身份认证
- 飞书用户ID验证
- JWT Token认证
- 用户角色权限控制

### 2. 数据安全
- 数据库连接加密
- 敏感信息加密存储
- SQL注入防护

### 3. 接口安全
- API限流
- 请求参数验证
- 错误信息脱敏

## 性能优化

### 1. 数据库优化
- **索引优化**: 基于PRD查询需求设计复合索引，支持500+任务和50+用户
- **查询优化**: 使用EXPLAIN分析查询计划，优化慢查询
- **连接池管理**: 配置PostgreSQL连接池，支持并发访问
- **分页查询**: 任务列表支持分页，每页20条记录，响应时间≤2秒
- **数据分区**: 大表按时间分区，提高查询效率

### 2. 缓存策略
- **Redis缓存**: 缓存热点数据，如用户会话、任务统计
- **查询结果缓存**: 缓存常用查询结果，减少数据库压力
- **会话状态缓存**: JWT Token缓存，提高认证效率
- **API响应缓存**: 缓存不经常变化的数据，如用户列表

### 3. 异步处理
- **飞书消息异步发送**: 使用消息队列，避免阻塞主流程
- **定时任务异步执行**: APScheduler异步执行提醒任务
- **日志记录异步处理**: 异步记录操作日志，不影响业务性能
- **数据导出异步处理**: 大文件导出使用后台任务

### 4. 性能监控
- **响应时间监控**: 监控API响应时间，确保≤2秒
- **数据库性能监控**: 监控查询执行时间和连接数
- **飞书API监控**: 监控飞书消息发送延迟，确保≤30秒
- **系统资源监控**: 监控CPU、内存、磁盘使用率

## 监控和日志

### 1. 系统监控
- 服务健康检查
- 数据库连接监控
- 飞书API调用监控

### 2. 业务监控
- 任务创建数量
- 提醒发送成功率
- 用户活跃度统计

### 3. 日志管理
- 操作日志记录
- 错误日志收集
- 性能日志分析

## 部署架构

### 1. 开发环境
```
开发机器 → Docker Compose → PostgreSQL + OpenWebUI + 飞书机器人
```

### 2. 生产环境
```
负载均衡器 → 应用服务器集群 → 数据库主从 → 监控系统
```

### 3. Docker配置
```yaml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg13
    environment:
      POSTGRES_DB: pm_agent
      POSTGRES_USER: pm_user
      POSTGRES_PASSWORD: pm_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  webui:
    build: .
    ports:
      - "8100:8000"
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://pm_user:pm_password@postgres:5432/pm_agent
      OPENAI_API_KEY: ${OPENAI_API_KEY}
  
  scheduler:
    build: .
    command: python scheduler.py
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://pm_user:pm_password@postgres:5432/pm_agent
  
  # 知识库服务 (未来扩展)
  knowledge_service:
    build: ./knowledge
    ports:
      - "8200:8000"
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://pm_user:pm_password@postgres:5432/pm_agent
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - ./knowledge/pmbok:/app/pmbok
      - ./knowledge/prince2:/app/prince2

volumes:
  postgres_data:
```

## 扩展性设计

### 1. 插件扩展
- 标准插件接口
- 插件热加载
- 插件配置管理

### 2. 数据库扩展
- 分表分库支持
- 读写分离
- 数据迁移工具

### 3. 服务扩展
- 微服务架构支持
- API网关集成
- 服务发现机制

## 开发规范

### 1. 代码规范
- PEP 8 Python代码规范
- 类型注解
- 文档字符串

### 2. 测试规范
- 单元测试覆盖率 > 80%
- 集成测试
- 性能测试

### 3. 版本控制
- Git Flow工作流
- 语义化版本号
- 变更日志维护

## 风险评估

### 1. 技术风险
- 飞书API变更风险
- 数据库性能瓶颈
- 第三方依赖风险

### 2. 业务风险
- 用户接受度风险
- 功能复杂度风险
- 数据安全风险

### 3. 应对策略
- 技术选型保守
- 功能迭代开发
- 安全审计机制

## 知识库架构设计 (未来扩展)

### 1. 知识库组件

#### 1.1 PMBOK 知识库
- **内容来源**: PMBOK指南第7版
- **知识分类**: 项目管理知识领域、过程组、工具与技术
- **应用场景**: 任务规划、进度管理、质量管理建议

#### 1.2 PRINCE2 知识库
- **内容来源**: PRINCE2方法论指南
- **知识分类**: 原则、主题、过程、角色与职责
- **应用场景**: 项目启动、阶段控制、风险管理

#### 1.3 向量数据库
- **技术选型**: pgvector (PostgreSQL扩展) 或 ChromaDB
- **功能**: 语义搜索、相似度匹配、知识推荐
- **优势**: 支持自然语言查询、上下文理解

### 2. 知识库集成架构

```
用户查询 → 自然语言处理 → 向量搜索 → 知识检索 → LLM生成 → 智能建议
```

#### 2.1 知识库服务
```python
class KnowledgeService:
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.llm_client = LLMClient()
        self.pmbok_loader = PMBOKLoader()
        self.prince2_loader = PRINCE2Loader()
    
    def load_knowledge_base(self):
        """加载知识库内容"""
        # 加载PMBOK和PRINCE2文档
        # 生成向量嵌入
        # 存储到向量数据库
        pass
    
    def search_knowledge(self, query, context=None):
        """搜索相关知识"""
        # 向量相似度搜索
        # 结合任务上下文
        # 返回相关知识点
        pass
    
    def generate_advice(self, task_context, knowledge_points):
        """生成智能建议"""
        # 基于知识库内容
        # 结合任务上下文
        # 生成个性化建议
        pass
```

### 3. 知识库应用场景

#### 3.1 任务创建建议
- **输入**: 任务描述、项目阶段
- **输出**: 基于PMBOK/PRINCE2的任务分解建议
- **示例**: "根据PRINCE2，这个阶段需要完成以下检查点..."

#### 3.2 风险管理建议
- **输入**: 项目风险描述
- **输出**: 基于方法论的风险应对策略
- **示例**: "根据PMBOK风险管理知识领域，建议采用..."

#### 3.3 进度管理建议
- **输入**: 项目进度情况
- **输出**: 进度控制最佳实践
- **示例**: "根据PRINCE2阶段控制原则，建议..."

### 4. 知识库数据流程

#### 4.1 知识库构建流程
```
文档解析 → 内容分块 → 向量化 → 存储索引 → 质量验证
```

#### 4.2 知识检索流程
```
用户查询 → 意图识别 → 向量搜索 → 结果排序 → 上下文增强 → 答案生成
```

### 5. 技术实现细节

#### 5.1 文档处理
- **格式支持**: PDF、Word、Markdown
- **内容提取**: 使用PyPDF2、python-docx等工具
- **文本分块**: 按章节、段落进行智能分割

#### 5.2 向量化处理
- **嵌入模型**: text-embedding-ada-002 或本地模型
- **向量维度**: 1536维 (OpenAI) 或 768维 (BERT)
- **相似度计算**: 余弦相似度

#### 5.3 检索优化
- **混合搜索**: 向量搜索 + 关键词搜索
- **重排序**: 基于相关性和质量的重排序
- **上下文窗口**: 动态调整上下文长度

### 6. 知识库部署方案

#### 6.1 开发环境
```yaml
knowledge_service:
  build: ./knowledge
  ports:
    - "8200:8000"
  environment:
    VECTOR_DB_URL: postgresql://pm_user:pm_password@postgres:5432/pm_agent
    OPENAI_API_KEY: ${OPENAI_API_KEY}
  volumes:
    - ./knowledge/pmbok:/app/pmbok
    - ./knowledge/prince2:/app/prince2
```

#### 6.2 生产环境
- **知识库更新**: 定期更新PMBOK/PRINCE2最新版本
- **性能优化**: 向量索引优化、缓存策略
- **监控告警**: 知识库服务健康检查、查询性能监控

### 7. 知识库扩展计划

#### 7.1 第一阶段 (MVP后)
- 基础PMBOK知识库集成
- 简单问答功能
- 任务创建建议

#### 7.2 第二阶段
- PRINCE2知识库集成
- 智能风险建议
- 进度管理指导

#### 7.3 第三阶段
- 自定义知识库
- 多语言支持
- 知识图谱构建

## 数据备份和恢复架构

### 1. 备份策略

#### 1.1 数据库备份
```bash
# 每日全量备份
pg_dump -h localhost -U pm_user -d pm_agent > backup_$(date +%Y%m%d).sql

# 每小时增量备份
pg_dump -h localhost -U pm_user -d pm_agent --data-only > incremental_$(date +%Y%m%d_%H).sql
```

#### 1.2 文件备份
- **知识库文件**: PMBOK/PRINCE2文档定期备份
- **导出文件**: 用户导出的Excel/PDF文件备份
- **配置文件**: 系统配置和环境变量备份

#### 1.3 备份存储
- **本地存储**: 开发环境本地备份
- **云存储**: 生产环境使用阿里云OSS/腾讯云COS
- **异地备份**: 重要数据异地存储

### 2. 恢复机制

#### 2.1 数据库恢复
```bash
# 全量恢复
psql -h localhost -U pm_user -d pm_agent < backup_20240101.sql

# 增量恢复
psql -h localhost -U pm_user -d pm_agent < incremental_20240101_10.sql
```

#### 2.2 任务恢复
- **软删除**: 任务标记为删除状态，不物理删除
- **历史记录**: 完整的任务变更历史
- **恢复接口**: 提供任务恢复API

### 3. 备份监控

#### 3.1 备份状态监控
- 备份任务执行状态
- 备份文件完整性检查
- 备份存储空间监控

#### 3.2 告警机制
- 备份失败告警
- 存储空间不足告警
- 恢复操作告警

## 可视化管理架构 (未来扩展)

### 1. 图表组件设计

#### 1.1 甘特图
```javascript
// 甘特图组件
class GanttChart {
  constructor(container, tasks) {
    this.container = container;
    this.tasks = tasks;
  }
  
  render() {
    // 使用ECharts或D3.js渲染甘特图
    // 支持任务依赖关系显示
    // 支持拖拽调整任务时间
  }
  
  updateTask(taskId, newData) {
    // 更新任务数据并重新渲染
  }
}
```

#### 1.2 燃尽图
```javascript
// 燃尽图组件
class BurndownChart {
  constructor(container, sprintData) {
    this.container = container;
    this.sprintData = sprintData;
  }
  
  render() {
    // 显示理想燃尽线和实际燃尽线
    // 支持多Sprint对比
  }
}
```

#### 1.3 任务看板
```javascript
// 看板组件
class TaskBoard {
  constructor(container, tasks) {
    this.container = container;
    this.tasks = tasks;
  }
  
  render() {
    // 按状态分列显示任务
    // 支持拖拽改变任务状态
  }
}
```

### 2. 数据可视化服务

#### 2.1 图表数据API
```python
class VisualizationService:
    def get_gantt_data(self, project_id):
        """获取甘特图数据"""
        pass
    
    def get_burndown_data(self, sprint_id):
        """获取燃尽图数据"""
        pass
    
    def get_kanban_data(self, project_id):
        """获取看板数据"""
        pass
```

#### 2.2 实时更新
- WebSocket连接实现图表实时更新
- 任务状态变更时自动刷新图表
- 支持多用户同时查看

### 3. 移动端支持

#### 3.1 响应式设计
- 图表自适应移动端屏幕
- 触摸操作支持
- 简化移动端界面

#### 3.2 飞书App集成
- 飞书小程序支持
- 移动端任务查看
- 推送通知集成

### 4. 可视化部署

#### 4.1 前端服务
```yaml
visualization_service:
  build: ./frontend
  ports:
    - "8300:3000"
  environment:
    API_BASE_URL: http://webui:8000
  volumes:
    - ./frontend:/app
```

#### 4.2 图表服务
```yaml
chart_service:
  build: ./charts
  ports:
    - "8400:8000"
  depends_on:
    - postgres
  environment:
    DATABASE_URL: postgresql://pm_user:pm_password@postgres:5432/pm_agent
```
