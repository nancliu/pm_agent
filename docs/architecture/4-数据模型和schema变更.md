# 4. 数据模型和Schema变更

### 4.1 新数据模型

#### 4.1.1 项目里程碑模型 (Project Milestones)

**目的**: 管理项目的重要节点和里程碑
**集成**: 与现有tasks表通过project_id关联

**关键属性**:
- milestone_id: SERIAL PRIMARY KEY - 里程碑唯一标识
- project_id: INTEGER REFERENCES projects(project_id) - 关联项目
- milestone_name: TEXT NOT NULL - 里程碑名称
- milestone_date: DATE NOT NULL - 里程碑日期
- status: TEXT DEFAULT 'pending' - 状态（pending/completed/delayed）
- description: TEXT - 里程碑描述
- created_at: TIMESTAMP DEFAULT now() - 创建时间
- updated_at: TIMESTAMP DEFAULT now() - 更新时间

**关系**:
- **与现有**: 通过project_id与projects表关联
- **与新**: 与milestone_tasks表关联（多对多关系）

#### 4.1.2 风险评估模型 (Risk Assessment)

**目的**: 项目风险识别、评估和跟踪
**集成**: 与现有tasks表关联，支持风险任务化

**关键属性**:
- risk_id: SERIAL PRIMARY KEY - 风险唯一标识
- project_id: INTEGER REFERENCES projects(project_id) - 关联项目
- risk_title: TEXT NOT NULL - 风险标题
- risk_description: TEXT - 风险描述
- probability: INTEGER CHECK (probability BETWEEN 1 AND 5) - 发生概率(1-5)
- impact: INTEGER CHECK (impact BETWEEN 1 AND 5) - 影响程度(1-5)
- risk_level: TEXT GENERATED ALWAYS AS (CASE WHEN probability * impact >= 20 THEN 'high' WHEN probability * impact >= 10 THEN 'medium' ELSE 'low' END) - 风险等级
- mitigation_plan: TEXT - 缓解计划
- status: TEXT DEFAULT 'open' - 状态（open/mitigated/closed）
- assigned_to: TEXT - 负责人
- due_date: DATE - 处理截止日期

**关系**:
- **与现有**: 通过project_id与projects表关联，通过assigned_to与users表关联
- **与新**: 与risk_mitigation_tasks表关联

### 4.2 Schema集成策略

**数据库变更要求**:
- **新表**: milestones, risks, risk_mitigation_tasks, milestone_tasks
- **修改表**: 无（保持向后兼容）
- **新索引**: 在project_id, status, due_date字段上创建索引
- **迁移策略**: 使用PostgreSQL迁移脚本，支持回滚

**向后兼容性**:
- 所有新表使用独立的命名空间，避免与现有表冲突
- 现有API保持不变，新功能通过新端点提供
- 现有数据查询不受影响
