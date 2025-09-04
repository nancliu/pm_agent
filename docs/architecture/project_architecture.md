# 项目管理 Agent MVP 项目架构文档

## 项目概述

**项目名称**: 项目管理 Agent MVP  
**项目类型**: 科研项目管理智能应用  
**技术架构**: OpenWebUI + PostgreSQL + 飞书机器人  
**开发模式**: 单人开发团队，MVP优先  
**目标用户**: 科研团队（50+用户）  
**数据规模**: 500+任务管理  
**性能目标**: 响应时间≤2秒，可用性99%  

## 项目目录结构

```
pm_agent/
├── docs/                           # 📚 项目文档
│   ├── requirements.md             # 需求分析文档
│   ├── user_stories.md             # 用户故事文档
│   ├── technical_architecture.md   # 技术架构文档
│   ├── project_architecture.md     # 项目架构文档（本文件）
│   ├── api_documentation.md        # API接口文档
│   └── deployment_guide.md         # 部署指南
│
├── backend/                        # 🔧 后端代码
│   ├── plugins/                    # OpenWebUI插件
│   │   └── pm_agent/              # 项目管理Agent插件
│   │       ├── __init__.py
│   │       ├── main.py            # 插件主入口
│   │       ├── plugin.yaml        # 插件配置文件
│   │       ├── requirements.txt   # 插件依赖
│   │       ├── core/              # 核心业务逻辑
│   │       │   ├── __init__.py
│   │       │   ├── agent.py       # Agent核心类
│   │       │   ├── task_manager.py # 任务管理器
│   │       │   ├── query_processor.py # 查询处理器
│   │       │   ├── reminder_service.py # 提醒服务
│   │       │   └── feishu_integration.py # 飞书集成
│   │       ├── tools/             # 工具函数
│   │       │   ├── __init__.py
│   │       │   ├── task_tools.py  # 任务相关工具
│   │       │   ├── query_tools.py # 查询相关工具
│   │       │   ├── reminder_tools.py # 提醒相关工具
│   │       │   ├── export_tools.py # 导出相关工具
│   │       │   └── user_tools.py  # 用户相关工具
│   │       ├── utils/             # 工具函数
│   │       │   ├── __init__.py
│   │       │   ├── nlp.py         # 自然语言处理
│   │       │   ├── validators.py  # 数据验证
│   │       │   ├── helpers.py     # 辅助函数
│   │       │   ├── database.py    # 数据库操作
│   │       │   └── config.py      # 配置管理
│   │       ├── models/            # 数据模型
│   │       │   ├── __init__.py
│   │       │   ├── task.py        # 任务模型
│   │       │   ├── user.py        # 用户模型
│   │       │   └── base.py        # 基础模型
│   │       └── tests/             # 插件测试
│   │           ├── __init__.py
│   │           ├── test_agent.py
│   │           ├── test_tasks.py
│   │           ├── test_queries.py
│   │           └── test_reminders.py
│   │
│   ├── core/                       # 核心服务
│   │   ├── __init__.py
│   │   ├── database.py            # 数据库连接和配置
│   │   ├── config.py              # 配置管理
│   │   ├── auth.py                # 认证和授权
│   │   ├── cache.py               # 缓存管理
│   │   └── exceptions.py          # 自定义异常
│   │
│   ├── services/                   # 业务服务
│   │   ├── __init__.py
│   │   ├── task_service.py        # 任务服务
│   │   ├── user_service.py        # 用户服务
│   │   ├── feishu_service.py      # 飞书服务
│   │   ├── export_service.py      # 导出服务
│   │   ├── backup_service.py      # 备份服务
│   │   ├── reminder_service.py    # 提醒服务
│   │   └── notification_service.py # 通知服务
│   │
│   ├── models/                     # 数据模型
│   │   ├── __init__.py
│   │   ├── task.py                # 任务模型
│   │   ├── user.py                # 用户模型
│   │   ├── session.py             # 会话模型
│   │   ├── log.py                 # 日志模型
│   │   └── base.py                # 基础模型
│   │
│   ├── database/                   # 数据库相关
│   │   ├── __init__.py
│   │   ├── migrations/            # 数据库迁移
│   │   │   ├── 001_initial_schema.sql
│   │   │   ├── 002_add_history_tables.sql
│   │   │   └── 003_add_export_tables.sql
│   │   ├── seeds/                 # 初始数据
│   │   │   └── initial_data.sql
│   │   └── backup/                # 备份脚本
│   │       ├── backup.sh
│   │       └── restore.sh
│   │
│   ├── scheduler/                  # 定时任务
│   │   ├── __init__.py
│   │   ├── reminder_scheduler.py  # 提醒调度器
│   │   └── backup_scheduler.py    # 备份调度器
│   │
│   └── requirements.txt            # Python依赖
│
├── frontend/                       # 🎨 前端代码
│   ├── public/                     # 静态资源
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   │
│   ├── src/                        # 源代码
│   │   ├── components/             # 组件
│   │   │   ├── common/            # 通用组件
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Loading.tsx
│   │   │   ├── task/              # 任务相关组件
│   │   │   │   ├── TaskList.tsx
│   │   │   │   ├── TaskForm.tsx
│   │   │   │   ├── TaskDetail.tsx
│   │   │   │   └── TaskCard.tsx
│   │   │   └── report/            # 报告相关组件
│   │   │       ├── ReportGenerator.tsx
│   │   │       └── ExportOptions.tsx
│   │   │
│   │   ├── pages/                  # 页面
│   │   │   ├── Dashboard.tsx      # 仪表板
│   │   │   ├── Tasks.tsx          # 任务管理
│   │   │   ├── Reports.tsx        # 报告生成
│   │   │   ├── Settings.tsx       # 系统设置
│   │   │   └── Users.tsx          # 用户管理
│   │   │
│   │   ├── services/               # 服务层
│   │   │   ├── api.ts             # API调用
│   │   │   ├── auth.ts            # 认证服务
│   │   │   └── storage.ts         # 本地存储
│   │   │
│   │   ├── hooks/                  # 自定义Hooks
│   │   │   ├── useTasks.ts
│   │   │   ├── useUsers.ts
│   │   │   └── useAuth.ts
│   │   │
│   │   ├── utils/                  # 工具函数
│   │   │   ├── constants.ts
│   │   │   ├── helpers.ts
│   │   │   └── validators.ts
│   │   │
│   │   ├── types/                  # 类型定义
│   │   │   ├── task.ts
│   │   │   ├── user.ts
│   │   │   └── api.ts
│   │   │
│   │   ├── styles/                 # 样式文件
│   │   │   ├── globals.css
│   │   │   ├── components.css
│   │   │   └── variables.css
│   │   │
│   │   ├── App.tsx                 # 应用主组件
│   │   └── index.tsx               # 应用入口
│   │
│   ├── package.json                # 前端依赖
│   ├── tsconfig.json               # TypeScript配置
│   ├── tailwind.config.js          # Tailwind配置
│   └── vite.config.ts              # Vite配置
│
├── knowledge/                      # 📖 知识库文件
│   ├── pmbok/                      # PMBOK知识库
│   │   ├── pmbok_guide_v7.pdf
│   │   ├── knowledge_points.json
│   │   └── embeddings/             # 向量嵌入
│   │
│   ├── prince2/                    # PRINCE2知识库
│   │   ├── prince2_guide.pdf
│   │   ├── methodology_points.json
│   │   └── embeddings/             # 向量嵌入
│   │
│   └── scripts/                    # 知识库处理脚本
│       ├── extract_knowledge.py
│       ├── generate_embeddings.py
│       └── build_index.py
│
├── scripts/                        # 🔧 部署和工具脚本
│   ├── setup/                      # 环境设置
│   │   ├── install_dependencies.sh
│   │   ├── setup_database.sh
│   │   └── configure_environment.sh
│   │
│   ├── deployment/                 # 部署脚本
│   │   ├── deploy_dev.sh
│   │   ├── deploy_prod.sh
│   │   └── rollback.sh
│   │
│   ├── maintenance/                # 维护脚本
│   │   ├── backup_database.sh
│   │   ├── cleanup_logs.sh
│   │   └── health_check.sh
│   │
│   └── development/                # 开发工具
│       ├── generate_migration.py
│       ├── seed_test_data.py
│       └── run_tests.sh
│
├── docker/                         # 🐳 Docker配置
│   ├── docker-compose.yml          # 开发环境
│   ├── docker-compose.prod.yml     # 生产环境
│   ├── Dockerfile.backend          # 后端镜像
│   ├── Dockerfile.frontend         # 前端镜像
│   └── nginx/                      # Nginx配置
│       ├── nginx.conf
│       └── ssl/                    # SSL证书
│
├── tests/                          # 🧪 测试代码
│   ├── unit/                       # 单元测试
│   │   ├── test_services/
│   │   ├── test_models/
│   │   └── test_utils/
│   │
│   ├── integration/                # 集成测试
│   │   ├── test_api/
│   │   ├── test_database/
│   │   └── test_feishu/
│   │
│   ├── e2e/                        # 端到端测试
│   │   ├── test_user_flows/
│   │   └── test_task_management/
│   │
│   ├── fixtures/                   # 测试数据
│   │   ├── test_tasks.json
│   │   └── test_users.json
│   │
│   └── conftest.py                 # 测试配置
│
├── logs/                           # 📝 日志文件
│   ├── application.log
│   ├── error.log
│   ├── access.log
│   └── scheduler.log
│
├── data/                           # 💾 数据文件
│   ├── exports/                    # 导出文件
│   ├── backups/                    # 备份文件
│   └── uploads/                    # 上传文件
│
├── .env.example                    # 环境变量示例
├── .env.local                      # 本地环境变量
├── .gitignore                      # Git忽略文件
├── .cursorrules                    # Cursor规则
├── README.md                       # 项目说明
├── CHANGELOG.md                    # 变更日志
└── LICENSE                         # 许可证
```

## 技术架构层次

### 1. 表示层 (Presentation Layer)
- **Web前端**: React/Vue.js + TypeScript
- **飞书机器人**: 自然语言交互界面
- **移动端**: 响应式设计 + 飞书App集成

### 2. 业务逻辑层 (Business Logic Layer)
- **OpenWebUI插件**: 核心业务逻辑处理
- **Agent系统**: 智能任务管理和建议
- **服务层**: 业务服务封装

### 3. 数据访问层 (Data Access Layer)
- **ORM**: SQLAlchemy数据模型
- **数据库**: PostgreSQL + pgvector
- **缓存**: Redis (可选)

### 4. 基础设施层 (Infrastructure Layer)
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **监控**: 日志收集和健康检查

## 核心组件设计

### 1. OpenWebUI插件架构
```python
# 插件主入口
class PMAgentPlugin(Plugin):
    def __init__(self):
        self.agent = ProjectManagementAgent()
        self.tools = [
            TaskCreationTool(),
            TaskQueryTool(),
            ReminderTool(),
            ExportTool()
        ]
    
    def handle_message(self, message, context):
        return self.agent.process_request(message, context)
```

### 2. 数据库设计
```sql
-- 核心表结构
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    assignee TEXT,
    start_date DATE,
    due_date DATE,
    status TEXT DEFAULT '未开始',
    priority TEXT DEFAULT '中',
    agent_type TEXT DEFAULT '进度',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- 支持表
CREATE TABLE users (...);
CREATE TABLE task_history (...);
CREATE TABLE export_records (...);
CREATE TABLE knowledge_base (...);
```

### 3. 服务层架构
```python
# 服务层设计
class TaskService:
    def create_task(self, task_data): pass
    def update_task(self, task_id, data): pass
    def delete_task(self, task_id): pass
    def get_tasks(self, filters): pass

class FeishuService:
    def send_message(self, user_id, message): pass
    def parse_natural_language(self, text): pass

class ReminderService:
    def schedule_reminder(self, task_id): pass
    def check_due_tasks(self): pass
```

## 开发流程

### 1. 环境设置
```bash
# 1. 克隆项目
git clone <repository-url>
cd pm_agent

# 2. 设置环境变量
cp .env.example .env.local

# 3. 安装依赖
./scripts/setup/install_dependencies.sh

# 4. 启动开发环境
docker-compose up -d
```

### 2. 开发工作流
```bash
# 1. 创建功能分支
git checkout -b feature/task-management

# 2. 开发功能
# 编写代码、测试、文档

# 3. 提交代码
git add .
git commit -m "feat: 添加任务管理功能"

# 4. 推送分支
git push origin feature/task-management

# 5. 创建Pull Request
# 代码审查、测试验证、合并
```

### 3. 测试流程
```bash
# 单元测试
python -m pytest tests/unit/

# 集成测试
python -m pytest tests/integration/

# 端到端测试
npm run test:e2e

# 性能测试
python -m pytest tests/performance/
```

## 部署架构

### 1. 开发环境
```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg13
    ports: ["5432:5432"]
  
  webui:
    build: ./backend
    ports: ["8100:8000"]
    depends_on: [postgres]
  
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [webui]
```

### 2. 生产环境
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg13
    volumes: [postgres_data:/var/lib/postgresql/data]
  
  webui:
    build: ./backend
    ports: ["8100:8000"]
    depends_on: [postgres]
    restart: unless-stopped
  
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [webui]
    restart: unless-stopped
  
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    depends_on: [frontend, webui]
    volumes: [./docker/nginx:/etc/nginx]
```

## 监控和运维

### 1. 健康检查
- 服务状态监控
- 数据库连接检查
- 飞书API可用性检查
- 定时任务执行状态

### 2. 日志管理
- 应用日志: 业务操作记录
- 错误日志: 异常和错误信息
- 访问日志: API调用记录
- 调度日志: 定时任务执行记录

### 3. 备份策略
- 数据库每日全量备份
- 配置文件定期备份
- 知识库文件备份
- 导出文件归档

## 安全设计

### 1. 数据安全
- 数据库连接加密
- 敏感信息加密存储
- SQL注入防护
- 输入参数验证

### 2. 接口安全
- JWT Token认证
- API限流控制
- 请求参数验证
- 错误信息脱敏

### 3. 权限管理
- 用户角色权限控制
- 操作日志记录
- 数据访问控制
- 跨团队数据隔离

## 性能优化

### 1. 数据库优化
- 合理的索引设计
- 查询语句优化
- 连接池管理
- 分页查询优化

### 2. 缓存策略
- 热点数据缓存
- 查询结果缓存
- 会话状态缓存
- 静态资源缓存

### 3. 异步处理
- 飞书消息异步发送
- 定时任务异步执行
- 日志记录异步处理
- 导出任务异步执行

## 扩展规划

### 1. 功能扩展
- 需求Agent集成
- 风险Agent集成
- 知识库智能问答
- 可视化图表展示

### 2. 技术扩展
- 微服务架构改造
- 分布式部署
- 高可用集群
- 负载均衡

### 3. 集成扩展
- 更多IM平台支持
- 第三方项目管理工具集成
- 企业系统集成
- API开放平台

## 开发规范

### 1. 代码规范
- Python: PEP 8 + 类型注解
- TypeScript: ESLint + Prettier
- SQL: 规范化命名和索引
- 文档: Markdown + 中文注释

### 2. 测试规范
- 单元测试覆盖率 > 80%
- 集成测试覆盖核心功能
- 性能测试验证非功能需求
- 所有API必须有测试用例

### 3. 部署规范
- 多环境配置管理
- 容器化部署
- 健康检查配置
- 监控告警设置

## 项目里程碑

### 第一阶段 (MVP核心功能)
- [ ] 基础插件架构搭建
- [ ] 任务管理功能实现
- [ ] 飞书机器人集成
- [ ] 定时提醒功能
- [ ] Web前端基础界面

### 第二阶段 (功能完善)
- [ ] 数据导出功能
- [ ] 用户管理功能
- [ ] 任务恢复功能
- [ ] 系统配置功能
- [ ] 性能优化

### 第三阶段 (系统优化)
- [ ] 知识库集成
- [ ] 可视化图表
- [ ] 移动端支持
- [ ] 高级功能
- [ ] 生产环境部署

这个架构设计为项目管理Agent提供了完整的开发框架，支持从MVP到完整产品的渐进式开发。
