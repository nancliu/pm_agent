# 项目管理 Agent MVP

基于OpenWebUI + PostgreSQL + 飞书机器人的科研项目管理智能应用，实现任务管理、进度跟踪、到期提醒等核心功能。

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd pm_agent
   ```

2. **安装Python依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   ```bash
   cp env.example .env
   # 编辑 .env 文件，填入实际配置
   ```

4. **启动数据库**
   ```bash
   docker-compose up -d postgres
   ```

5. **运行数据库迁移**
   ```bash
   python backend/plugins/pm_agent/migrations.py
   ```

6. **启动应用**
   ```bash
   python backend/plugins/pm_agent/main.py
   ```

7. **访问应用**
   - API文档: http://localhost:8000/docs
   - 健康检查: http://localhost:8000/api/pm_agent/health

## 📁 项目结构

```
pm_agent/
├── backend/                    # 后端代码
│   ├── plugins/
│   │   └── pm_agent/          # OpenWebUI插件
│   │       ├── __init__.py
│   │       ├── main.py        # 主应用
│   │       ├── config.py      # 配置管理
│   │       ├── database.py    # 数据库连接
│   │       ├── models.py      # 数据模型
│   │       ├── schemas.py     # Pydantic模式
│   │       ├── routes.py      # API路由
│   │       ├── migrations.py  # 数据库迁移
│   │       └── plugin.yaml    # 插件配置
│   ├── core/                  # 核心业务逻辑
│   ├── services/              # 业务服务
│   ├── models/                # 数据模型
│   ├── database/              # 数据库相关
│   └── utils/                 # 工具函数
├── frontend/                  # 前端代码
├── tests/                     # 测试代码
│   ├── unit/                  # 单元测试
│   └── integration/           # 集成测试
├── docs/                      # 项目文档
├── docker/                    # Docker配置
│   └── postgres/
│       └── init/              # 数据库初始化脚本
├── docker-compose.yml         # Docker Compose配置
├── requirements.txt           # Python依赖
├── env.example               # 环境变量示例
└── README.md                 # 项目说明
```

## 🛠️ 技术栈

- **后端**: OpenWebUI + FastAPI + Python 3.9+
- **数据库**: PostgreSQL 15+ (Docker)
- **前端**: React/Vue.js + OpenWebUI UI组件
- **部署**: Docker + Docker Compose
- **测试**: pytest + pytest-asyncio

## 📊 数据库设计

### 核心表结构

- **users**: 用户表
  - id, username, email, password_hash, role, status, created_at, updated_at

- **tasks**: 任务表
  - id, title, description, assignee_id, due_date, priority, status, created_by, created_at, updated_at, deleted_at

- **task_history**: 任务历史记录表
  - id, task_id, field_name, old_value, new_value, changed_by, changed_at

## 🔧 开发指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 生成测试覆盖率报告
pytest --cov=backend tests/
```

### 代码格式化

```bash
# 格式化Python代码
black backend/
isort backend/

# 代码检查
ruff check backend/
```

### 数据库管理

```bash
# 连接数据库
docker exec -it pm_agent_postgres psql -U pm_user -d pm_agent

# 查看表结构
\dt

# 查看数据
SELECT * FROM users;
SELECT * FROM tasks;
```

## 🚀 部署

### Docker部署

```bash
# 构建镜像
docker build -t pm-agent .

# 运行容器
docker run -d -p 8000:8000 pm-agent
```

### 生产环境配置

1. 修改 `.env` 文件中的生产环境配置
2. 设置强密码和密钥
3. 配置HTTPS
4. 设置日志轮转
5. 配置监控和告警

## 📝 API文档

启动应用后访问 http://localhost:8000/docs 查看完整的API文档。

### 主要端点

- `GET /api/pm_agent/health` - 健康检查
- `GET /api/pm_agent/tasks` - 获取任务列表
- `POST /api/pm_agent/tasks` - 创建任务
- `PUT /api/pm_agent/tasks/{task_id}` - 更新任务
- `DELETE /api/pm_agent/tasks/{task_id}` - 删除任务

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如有问题或建议，请提交 Issue 或联系开发团队。

---

**开发状态**: 🚧 开发中  
**版本**: 1.0.0  
**最后更新**: 2024-01-15
