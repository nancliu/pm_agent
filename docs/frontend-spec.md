# 项目管理 Agent MVP 前端开发规范

## 文档概述

**文档类型**: 前端开发规范  
**适用项目**: 项目管理 Agent MVP  
**技术栈**: React + TypeScript + Ant Design  
**目标用户**: 科研团队（50+用户）  
**性能要求**: 响应时间≤2秒，支持500+任务管理  

## 技术栈选型

### 核心框架
- **React 18+**: 函数式组件 + Hooks
- **TypeScript 4.9+**: 类型安全开发
- **Vite 4+**: 快速构建工具
- **Ant Design 5+**: UI组件库

### 状态管理
- **Zustand**: 轻量级状态管理
- **React Query**: 服务端状态管理
- **Context API**: 全局状态共享

### 样式方案
- **Ant Design**: 基础组件样式
- **CSS Modules**: 组件级样式隔离
- **Styled Components**: 动态样式
- **Tailwind CSS**: 工具类样式（可选）

### 工具库
- **Axios**: HTTP客户端
- **Day.js**: 日期处理
- **Lodash**: 工具函数
- **React Hook Form**: 表单管理
- **React Router**: 路由管理

## 项目结构规范

### 目录结构
```
frontend/
├── public/                     # 静态资源
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
│
├── src/                        # 源代码
│   ├── components/             # 组件
│   │   ├── common/            # 通用组件
│   │   │   ├── Header/
│   │   │   │   ├── index.tsx
│   │   │   │   ├── Header.module.css
│   │   │   │   └── types.ts
│   │   │   ├── Sidebar/
│   │   │   ├── Loading/
│   │   │   ├── ErrorBoundary/
│   │   │   └── ConfirmDialog/
│   │   │
│   │   ├── task/              # 任务相关组件
│   │   │   ├── TaskList/
│   │   │   │   ├── index.tsx
│   │   │   │   ├── TaskList.module.css
│   │   │   │   ├── types.ts
│   │   │   │   └── hooks.ts
│   │   │   ├── TaskForm/
│   │   │   ├── TaskDetail/
│   │   │   ├── TaskCard/
│   │   │   └── TaskFilter/
│   │   │
│   │   ├── user/              # 用户相关组件
│   │   │   ├── UserList/
│   │   │   ├── UserForm/
│   │   │   └── UserSelect/
│   │   │
│   │   ├── report/            # 报告相关组件
│   │   │   ├── ReportGenerator/
│   │   │   ├── ExportOptions/
│   │   │   └── ChartView/
│   │   │
│   │   └── layout/            # 布局组件
│   │       ├── MainLayout/
│   │       ├── AuthLayout/
│   │       └── PageLayout/
│   │
│   ├── pages/                  # 页面组件
│   │   ├── Dashboard/
│   │   │   ├── index.tsx
│   │   │   ├── Dashboard.module.css
│   │   │   └── hooks.ts
│   │   ├── Tasks/
│   │   ├── Reports/
│   │   ├── Settings/
│   │   ├── Users/
│   │   └── Login/
│   │
│   ├── hooks/                  # 自定义Hooks
│   │   ├── useTasks.ts
│   │   ├── useUsers.ts
│   │   ├── useAuth.ts
│   │   ├── useLocalStorage.ts
│   │   └── useDebounce.ts
│   │
│   ├── services/               # 服务层
│   │   ├── api/
│   │   │   ├── index.ts
│   │   │   ├── taskApi.ts
│   │   │   ├── userApi.ts
│   │   │   └── authApi.ts
│   │   ├── auth.ts
│   │   ├── storage.ts
│   │   └── notification.ts
│   │
│   ├── stores/                 # 状态管理
│   │   ├── authStore.ts
│   │   ├── taskStore.ts
│   │   ├── userStore.ts
│   │   └── uiStore.ts
│   │
│   ├── utils/                  # 工具函数
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   ├── validators.ts
│   │   ├── formatters.ts
│   │   └── dateUtils.ts
│   │
│   ├── types/                  # 类型定义
│   │   ├── task.ts
│   │   ├── user.ts
│   │   ├── api.ts
│   │   ├── common.ts
│   │   └── index.ts
│   │
│   ├── styles/                 # 样式文件
│   │   ├── globals.css
│   │   ├── variables.css
│   │   ├── antd-custom.css
│   │   └── components.css
│   │
│   ├── assets/                 # 静态资源
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── App.tsx                 # 应用主组件
│   ├── main.tsx                # 应用入口
│   └── router.tsx              # 路由配置
│
├── package.json                # 依赖配置
├── tsconfig.json               # TypeScript配置
├── vite.config.ts              # Vite配置
├── tailwind.config.js          # Tailwind配置
├── .eslintrc.js                # ESLint配置
├── .prettierrc                 # Prettier配置
└── README.md                   # 项目说明
```

## 代码规范

### 1. 命名规范

#### 文件命名
- **组件文件**: PascalCase (如 `TaskList.tsx`)
- **工具文件**: camelCase (如 `dateUtils.ts`)
- **样式文件**: kebab-case (如 `task-list.module.css`)
- **常量文件**: UPPER_SNAKE_CASE (如 `API_CONSTANTS.ts`)

#### 变量命名
```typescript
// 组件名使用PascalCase
const TaskList = () => {};

// 变量和函数使用camelCase
const taskList = [];
const handleTaskClick = () => {};

// 常量使用UPPER_SNAKE_CASE
const API_BASE_URL = 'https://api.example.com';

// 接口和类型使用PascalCase
interface TaskItem {
  id: string;
  title: string;
}

// 枚举使用PascalCase
enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed'
}
```

#### 组件命名
```typescript
// 组件文件命名
TaskList.tsx          // 任务列表组件
TaskForm.tsx          // 任务表单组件
TaskCard.tsx          // 任务卡片组件

// 组件内部命名
const TaskList = () => {};           // 主组件
const TaskListItem = () => {};       // 子组件
const useTaskList = () => {};        // 自定义Hook
```

### 2. 组件开发规范

#### 函数式组件结构
```typescript
import React, { useState, useEffect, useCallback } from 'react';
import { Button, Table, Modal } from 'antd';
import { TaskItem, TaskStatus } from '@/types/task';
import { useTaskList } from '@/hooks/useTasks';
import styles from './TaskList.module.css';

interface TaskListProps {
  userId?: string;
  status?: TaskStatus;
  onTaskSelect?: (task: TaskItem) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  userId,
  status,
  onTaskSelect
}) => {
  // 1. 状态定义
  const [selectedTasks, setSelectedTasks] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  
  // 2. 自定义Hooks
  const { tasks, error, refetch } = useTaskList({ userId, status });
  
  // 3. 事件处理函数
  const handleTaskClick = useCallback((task: TaskItem) => {
    onTaskSelect?.(task);
  }, [onTaskSelect]);
  
  const handleBatchDelete = useCallback(async () => {
    // 批量删除逻辑
  }, [selectedTasks]);
  
  // 4. 副作用
  useEffect(() => {
    refetch();
  }, [userId, status, refetch]);
  
  // 5. 渲染逻辑
  if (error) {
    return <div>加载失败: {error.message}</div>;
  }
  
  return (
    <div className={styles.container}>
      <Table
        dataSource={tasks}
        loading={loading}
        onRow={(record) => ({
          onClick: () => handleTaskClick(record)
        })}
        // ... 其他props
      />
    </div>
  );
};

export default TaskList;
```

#### 组件Props规范
```typescript
// 1. 必须定义Props接口
interface TaskFormProps {
  // 必需属性
  task: TaskItem;
  onSubmit: (task: TaskItem) => void;
  
  // 可选属性
  onCancel?: () => void;
  loading?: boolean;
  
  // 样式相关
  className?: string;
  style?: React.CSSProperties;
}

// 2. 使用默认值
const TaskForm: React.FC<TaskFormProps> = ({
  task,
  onSubmit,
  onCancel,
  loading = false,
  className = '',
  style
}) => {
  // 组件实现
};
```

#### 自定义Hook规范
```typescript
// hooks/useTasks.ts
import { useState, useEffect, useCallback } from 'react';
import { TaskItem, TaskFilters } from '@/types/task';
import { taskApi } from '@/services/api/taskApi';

interface UseTasksOptions {
  userId?: string;
  status?: string;
  autoFetch?: boolean;
}

interface UseTasksReturn {
  tasks: TaskItem[];
  loading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
  createTask: (task: Omit<TaskItem, 'id'>) => Promise<void>;
  updateTask: (id: string, task: Partial<TaskItem>) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
}

export const useTasks = (options: UseTasksOptions = {}): UseTasksReturn => {
  const { userId, status, autoFetch = true } = options;
  
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await taskApi.getTasks({ userId, status });
      setTasks(data);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, [userId, status]);
  
  const createTask = useCallback(async (task: Omit<TaskItem, 'id'>) => {
    try {
      const newTask = await taskApi.createTask(task);
      setTasks(prev => [...prev, newTask]);
    } catch (err) {
      setError(err as Error);
      throw err;
    }
  }, []);
  
  useEffect(() => {
    if (autoFetch) {
      fetchTasks();
    }
  }, [fetchTasks, autoFetch]);
  
  return {
    tasks,
    loading,
    error,
    refetch: fetchTasks,
    createTask,
    updateTask: async (id, task) => {
      // 实现更新逻辑
    },
    deleteTask: async (id) => {
      // 实现删除逻辑
    }
  };
};
```

### 3. 类型定义规范

#### 基础类型定义
```typescript
// types/task.ts
export interface TaskItem {
  id: string;
  title: string;
  description?: string;
  assigneeId: string;
  assigneeName: string;
  startDate?: string;
  dueDate: string;
  status: TaskStatus;
  priority: TaskPriority;
  agentType: AgentType;
  createdAt: string;
  updatedAt: string;
}

export enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  OVERDUE = 'overdue'
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

export enum AgentType {
  PROGRESS = 'progress',
  REQUIREMENT = 'requirement',
  RISK = 'risk'
}

export interface TaskFilters {
  userId?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  assigneeId?: string;
  startDate?: string;
  endDate?: string;
  keyword?: string;
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  assigneeId: string;
  startDate?: string;
  dueDate: string;
  priority: TaskPriority;
  agentType: AgentType;
}

export interface UpdateTaskRequest extends Partial<CreateTaskRequest> {
  id: string;
  status?: TaskStatus;
}
```

#### API响应类型
```typescript
// types/api.ts
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  code?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasNext: boolean;
  hasPrev: boolean;
}

export interface ApiError {
  message: string;
  code: number;
  details?: Record<string, any>;
}
```

### 4. 样式规范

#### CSS Modules使用
```css
/* TaskList.module.css */
.container {
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #262626;
}

.actions {
  display: flex;
  gap: 8px;
}

.table {
  margin-top: 16px;
}

.statusPending {
  color: #faad14;
}

.statusCompleted {
  color: #52c41a;
}

.statusOverdue {
  color: #ff4d4f;
}

@media (max-width: 768px) {
  .container {
    padding: 12px;
  }
  
  .header {
    flex-direction: column;
    gap: 12px;
  }
}
```

#### 全局样式变量
```css
/* styles/variables.css */
:root {
  /* 主色调 */
  --primary-color: #1890ff;
  --primary-hover: #40a9ff;
  --primary-active: #096dd9;
  
  /* 功能色 */
  --success-color: #52c41a;
  --warning-color: #faad14;
  --error-color: #ff4d4f;
  --info-color: #1890ff;
  
  /* 中性色 */
  --text-primary: #262626;
  --text-secondary: #595959;
  --text-disabled: #bfbfbf;
  --border-color: #d9d9d9;
  --background-color: #f5f5f5;
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  /* 圆角 */
  --border-radius-sm: 4px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  
  /* 阴影 */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.1);
}
```

### 5. 状态管理规范

#### Zustand Store设计
```typescript
// stores/taskStore.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { TaskItem, TaskFilters } from '@/types/task';

interface TaskState {
  // 状态
  tasks: TaskItem[];
  selectedTasks: string[];
  filters: TaskFilters;
  loading: boolean;
  error: string | null;
  
  // 操作
  setTasks: (tasks: TaskItem[]) => void;
  addTask: (task: TaskItem) => void;
  updateTask: (id: string, task: Partial<TaskItem>) => void;
  removeTask: (id: string) => void;
  setSelectedTasks: (ids: string[]) => void;
  setFilters: (filters: Partial<TaskFilters>) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useTaskStore = create<TaskState>()(
  devtools(
    (set, get) => ({
      // 初始状态
      tasks: [],
      selectedTasks: [],
      filters: {},
      loading: false,
      error: null,
      
      // 操作实现
      setTasks: (tasks) => set({ tasks }),
      
      addTask: (task) => set((state) => ({
        tasks: [...state.tasks, task]
      })),
      
      updateTask: (id, updates) => set((state) => ({
        tasks: state.tasks.map(task =>
          task.id === id ? { ...task, ...updates } : task
        )
      })),
      
      removeTask: (id) => set((state) => ({
        tasks: state.tasks.filter(task => task.id !== id),
        selectedTasks: state.selectedTasks.filter(taskId => taskId !== id)
      })),
      
      setSelectedTasks: (ids) => set({ selectedTasks: ids }),
      
      setFilters: (filters) => set((state) => ({
        filters: { ...state.filters, ...filters }
      })),
      
      setLoading: (loading) => set({ loading }),
      
      setError: (error) => set({ error }),
      
      clearError: () => set({ error: null })
    }),
    {
      name: 'task-store'
    }
  )
);
```

### 6. API服务规范

#### API服务封装
```typescript
// services/api/taskApi.ts
import axios from 'axios';
import { TaskItem, CreateTaskRequest, UpdateTaskRequest, TaskFilters, PaginatedResponse } from '@/types/task';
import { ApiResponse } from '@/types/api';

class TaskApi {
  private baseURL = '/api/tasks';
  
  async getTasks(filters?: TaskFilters): Promise<TaskItem[]> {
    const response = await axios.get<ApiResponse<TaskItem[]>>(this.baseURL, {
      params: filters
    });
    return response.data.data;
  }
  
  async getTaskById(id: string): Promise<TaskItem> {
    const response = await axios.get<ApiResponse<TaskItem>>(`${this.baseURL}/${id}`);
    return response.data.data;
  }
  
  async createTask(task: CreateTaskRequest): Promise<TaskItem> {
    const response = await axios.post<ApiResponse<TaskItem>>(this.baseURL, task);
    return response.data.data;
  }
  
  async updateTask(id: string, task: UpdateTaskRequest): Promise<TaskItem> {
    const response = await axios.put<ApiResponse<TaskItem>>(`${this.baseURL}/${id}`, task);
    return response.data.data;
  }
  
  async deleteTask(id: string): Promise<void> {
    await axios.delete(`${this.baseURL}/${id}`);
  }
  
  async getTasksPaginated(
    page: number = 1,
    pageSize: number = 20,
    filters?: TaskFilters
  ): Promise<PaginatedResponse<TaskItem>> {
    const response = await axios.get<ApiResponse<PaginatedResponse<TaskItem>>>(
      `${this.baseURL}/paginated`,
      {
        params: { page, pageSize, ...filters }
      }
    );
    return response.data.data;
  }
}

export const taskApi = new TaskApi();
```

#### 请求拦截器配置
```typescript
// services/api/index.ts
import axios from 'axios';
import { message } from 'antd';
import { authStore } from '@/stores/authStore';

// 创建axios实例
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = authStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      authStore.getState().logout();
      message.error('登录已过期，请重新登录');
    } else if (error.response?.status >= 500) {
      message.error('服务器错误，请稍后重试');
    } else {
      message.error(error.response?.data?.message || '请求失败');
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 7. 路由配置规范

#### 路由结构设计
```typescript
// router.tsx
import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { MainLayout } from '@/components/layout/MainLayout';
import { AuthLayout } from '@/components/layout/AuthLayout';
import { Dashboard } from '@/pages/Dashboard';
import { Tasks } from '@/pages/Tasks';
import { Reports } from '@/pages/Reports';
import { Settings } from '@/pages/Settings';
import { Users } from '@/pages/Users';
import { Login } from '@/pages/Login';
import { ProtectedRoute } from '@/components/common/ProtectedRoute';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/dashboard" replace />
  },
  {
    path: '/login',
    element: (
      <AuthLayout>
        <Login />
      </AuthLayout>
    )
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <MainLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: 'dashboard',
        element: <Dashboard />
      },
      {
        path: 'tasks',
        element: <Tasks />
      },
      {
        path: 'tasks/:id',
        element: <TaskDetail />
      },
      {
        path: 'reports',
        element: <Reports />
      },
      {
        path: 'settings',
        element: <Settings />
      },
      {
        path: 'users',
        element: <Users />
      }
    ]
  },
  {
    path: '*',
    element: <Navigate to="/dashboard" replace />
  }
]);
```

#### 路由守卫组件
```typescript
// components/common/ProtectedRoute.tsx
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, loading } = useAuthStore();
  const location = useLocation();
  
  if (loading) {
    return <div>加载中...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  return <>{children}</>;
};
```

### 8. 表单处理规范

#### React Hook Form使用
```typescript
// components/task/TaskForm.tsx
import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Form, Input, Select, DatePicker, Button, Space } from 'antd';
import { TaskItem, CreateTaskRequest } from '@/types/task';
import { useUsers } from '@/hooks/useUsers';
import { taskFormSchema } from '@/utils/validators';

interface TaskFormProps {
  task?: TaskItem;
  onSubmit: (data: CreateTaskRequest) => void;
  onCancel: () => void;
  loading?: boolean;
}

const TaskForm: React.FC<TaskFormProps> = ({
  task,
  onSubmit,
  onCancel,
  loading = false
}) => {
  const { users } = useUsers();
  const { control, handleSubmit, formState: { errors } } = useForm<CreateTaskRequest>({
    defaultValues: task ? {
      title: task.title,
      description: task.description,
      assigneeId: task.assigneeId,
      startDate: task.startDate,
      dueDate: task.dueDate,
      priority: task.priority,
      agentType: task.agentType
    } : {
      priority: 'medium',
      agentType: 'progress'
    }
  });
  
  return (
    <Form
      layout="vertical"
      onFinish={handleSubmit(onSubmit)}
    >
      <Controller
        name="title"
        control={control}
        rules={{ required: '任务标题不能为空' }}
        render={({ field }) => (
          <Form.Item
            label="任务标题"
            validateStatus={errors.title ? 'error' : ''}
            help={errors.title?.message}
          >
            <Input {...field} placeholder="请输入任务标题" />
          </Form.Item>
        )}
      />
      
      <Controller
        name="description"
        control={control}
        render={({ field }) => (
          <Form.Item label="任务描述">
            <Input.TextArea
              {...field}
              rows={4}
              placeholder="请输入任务描述"
            />
          </Form.Item>
        )}
      />
      
      <Controller
        name="assigneeId"
        control={control}
        rules={{ required: '请选择负责人' }}
        render={({ field }) => (
          <Form.Item
            label="负责人"
            validateStatus={errors.assigneeId ? 'error' : ''}
            help={errors.assigneeId?.message}
          >
            <Select
              {...field}
              placeholder="请选择负责人"
              options={users.map(user => ({
                label: user.name,
                value: user.id
              }))}
            />
          </Form.Item>
        )}
      />
      
      <Space>
        <Controller
          name="startDate"
          control={control}
          render={({ field }) => (
            <Form.Item label="开始日期">
              <DatePicker {...field} />
            </Form.Item>
          )}
        />
        
        <Controller
          name="dueDate"
          control={control}
          rules={{ required: '截止日期不能为空' }}
          render={({ field }) => (
            <Form.Item
              label="截止日期"
              validateStatus={errors.dueDate ? 'error' : ''}
              help={errors.dueDate?.message}
            >
              <DatePicker {...field} />
            </Form.Item>
          )}
        />
      </Space>
      
      <Space>
        <Controller
          name="priority"
          control={control}
          render={({ field }) => (
            <Form.Item label="优先级">
              <Select
                {...field}
                options={[
                  { label: '低', value: 'low' },
                  { label: '中', value: 'medium' },
                  { label: '高', value: 'high' }
                ]}
              />
            </Form.Item>
          )}
        />
        
        <Controller
          name="agentType"
          control={control}
          render={({ field }) => (
            <Form.Item label="Agent类型">
              <Select
                {...field}
                options={[
                  { label: '进度', value: 'progress' },
                  { label: '需求', value: 'requirement' },
                  { label: '风险', value: 'risk' }
                ]}
              />
            </Form.Item>
          )}
        />
      </Space>
      
      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" loading={loading}>
            {task ? '更新' : '创建'}
          </Button>
          <Button onClick={onCancel}>
            取消
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default TaskForm;
```

### 9. 错误处理规范

#### 错误边界组件
```typescript
// components/common/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Result, Button } from 'antd';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    // 这里可以添加错误上报逻辑
  }
  
  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }
      
      return (
        <Result
          status="500"
          title="页面出现错误"
          subTitle="抱歉，页面遇到了一些问题。"
          extra={
            <Button
              type="primary"
              onClick={() => this.setState({ hasError: false })}
            >
              重试
            </Button>
          }
        />
      );
    }
    
    return this.props.children;
  }
}
```

#### 全局错误处理
```typescript
// utils/errorHandler.ts
import { message, notification } from 'antd';

export interface AppError {
  code: string;
  message: string;
  details?: any;
}

export class ErrorHandler {
  static handle(error: any): AppError {
    let appError: AppError;
    
    if (error.response) {
      // API错误
      appError = {
        code: error.response.data?.code || 'API_ERROR',
        message: error.response.data?.message || '请求失败',
        details: error.response.data
      };
    } else if (error.request) {
      // 网络错误
      appError = {
        code: 'NETWORK_ERROR',
        message: '网络连接失败，请检查网络设置',
        details: error.request
      };
    } else {
      // 其他错误
      appError = {
        code: 'UNKNOWN_ERROR',
        message: error.message || '未知错误',
        details: error
      };
    }
    
    // 根据错误类型显示不同的提示
    this.showError(appError);
    
    return appError;
  }
  
  private static showError(error: AppError) {
    switch (error.code) {
      case 'AUTH_ERROR':
        message.error('认证失败，请重新登录');
        break;
      case 'NETWORK_ERROR':
        notification.error({
          message: '网络错误',
          description: error.message,
          duration: 5
        });
        break;
      case 'VALIDATION_ERROR':
        message.error(error.message);
        break;
      default:
        message.error(error.message);
    }
  }
}
```

### 10. 性能优化规范

#### 组件优化
```typescript
// 使用React.memo优化组件
const TaskCard = React.memo<TaskCardProps>(({ task, onUpdate, onDelete }) => {
  const handleUpdate = useCallback((updates: Partial<TaskItem>) => {
    onUpdate(task.id, updates);
  }, [task.id, onUpdate]);
  
  const handleDelete = useCallback(() => {
    onDelete(task.id);
  }, [task.id, onDelete]);
  
  return (
    <div className={styles.card}>
      {/* 组件内容 */}
    </div>
  );
});

// 使用useMemo优化计算
const TaskList = () => {
  const { tasks, filters } = useTaskStore();
  
  const filteredTasks = useMemo(() => {
    return tasks.filter(task => {
      if (filters.status && task.status !== filters.status) return false;
      if (filters.priority && task.priority !== filters.priority) return false;
      if (filters.keyword && !task.title.includes(filters.keyword)) return false;
      return true;
    });
  }, [tasks, filters]);
  
  return (
    <div>
      {filteredTasks.map(task => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
};

// 使用useCallback优化事件处理
const TaskForm = () => {
  const { createTask } = useTaskStore();
  
  const handleSubmit = useCallback(async (data: CreateTaskRequest) => {
    try {
      await createTask(data);
      message.success('任务创建成功');
    } catch (error) {
      ErrorHandler.handle(error);
    }
  }, [createTask]);
  
  return (
    <form onSubmit={handleSubmit}>
      {/* 表单内容 */}
    </form>
  );
};
```

#### 虚拟滚动优化
```typescript
// components/task/VirtualizedTaskList.tsx
import { FixedSizeList as List } from 'react-window';

interface VirtualizedTaskListProps {
  tasks: TaskItem[];
  height: number;
}

const VirtualizedTaskList: React.FC<VirtualizedTaskListProps> = ({
  tasks,
  height
}) => {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      <TaskCard task={tasks[index]} />
    </div>
  );
  
  return (
    <List
      height={height}
      itemCount={tasks.length}
      itemSize={120} // 每个任务卡片的高度
      width="100%"
    >
      {Row}
    </List>
  );
};
```

### 11. 测试规范

#### 组件测试
```typescript
// components/task/__tests__/TaskCard.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from '../TaskCard';
import { TaskItem, TaskStatus } from '@/types/task';

const mockTask: TaskItem = {
  id: '1',
  title: '测试任务',
  description: '这是一个测试任务',
  assigneeId: 'user1',
  assigneeName: '张三',
  dueDate: '2024-01-01',
  status: TaskStatus.PENDING,
  priority: 'medium',
  agentType: 'progress',
  createdAt: '2024-01-01T00:00:00Z',
  updatedAt: '2024-01-01T00:00:00Z'
};

describe('TaskCard', () => {
  it('应该正确渲染任务信息', () => {
    render(<TaskCard task={mockTask} />);
    
    expect(screen.getByText('测试任务')).toBeInTheDocument();
    expect(screen.getByText('张三')).toBeInTheDocument();
    expect(screen.getByText('2024-01-01')).toBeInTheDocument();
  });
  
  it('应该正确处理点击事件', () => {
    const onUpdate = jest.fn();
    const onDelete = jest.fn();
    
    render(
      <TaskCard
        task={mockTask}
        onUpdate={onUpdate}
        onDelete={onDelete}
      />
    );
    
    fireEvent.click(screen.getByText('编辑'));
    expect(onUpdate).toHaveBeenCalled();
  });
});
```

#### Hook测试
```typescript
// hooks/__tests__/useTasks.test.ts
import { renderHook, act } from '@testing-library/react';
import { useTasks } from '../useTasks';
import { taskApi } from '@/services/api/taskApi';

jest.mock('@/services/api/taskApi');

describe('useTasks', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('应该正确获取任务列表', async () => {
    const mockTasks = [mockTask];
    (taskApi.getTasks as jest.Mock).mockResolvedValue(mockTasks);
    
    const { result } = renderHook(() => useTasks());
    
    await act(async () => {
      await result.current.refetch();
    });
    
    expect(result.current.tasks).toEqual(mockTasks);
    expect(result.current.loading).toBe(false);
  });
  
  it('应该正确处理创建任务', async () => {
    const newTask = { ...mockTask, id: '2' };
    (taskApi.createTask as jest.Mock).mockResolvedValue(newTask);
    
    const { result } = renderHook(() => useTasks());
    
    await act(async () => {
      await result.current.createTask({
        title: '新任务',
        assigneeId: 'user1',
        dueDate: '2024-01-01',
        priority: 'medium',
        agentType: 'progress'
      });
    });
    
    expect(result.current.tasks).toContain(newTask);
  });
});
```

### 12. 构建和部署规范

#### Vite配置
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8100',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          antd: ['antd'],
          utils: ['lodash', 'dayjs']
        }
      }
    }
  }
});
```

#### 环境配置
```typescript
// 环境变量配置
// .env.development
REACT_APP_API_BASE_URL=http://localhost:8100/api
REACT_APP_ENV=development

// .env.production
REACT_APP_API_BASE_URL=https://api.pm-agent.com/api
REACT_APP_ENV=production
```

### 13. 代码质量规范

#### ESLint配置
```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'react-app',
    'react-app/jest',
    '@typescript-eslint/recommended'
  ],
  rules: {
    'react-hooks/exhaustive-deps': 'warn',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    'prefer-const': 'error',
    'no-var': 'error'
  }
};
```

#### Prettier配置
```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
```

## 最佳实践

### 1. 组件设计原则
- **单一职责**: 每个组件只负责一个功能
- **可复用性**: 组件应该可以在不同场景下复用
- **可测试性**: 组件应该易于测试
- **可维护性**: 组件代码应该清晰易懂

### 2. 性能优化建议
- 使用React.memo避免不必要的重渲染
- 使用useMemo和useCallback优化计算和函数
- 实现虚拟滚动处理大量数据
- 使用代码分割减少初始加载时间

### 3. 错误处理策略
- 实现全局错误边界
- 提供友好的错误提示
- 记录错误日志用于调试
- 提供错误恢复机制

### 4. 可访问性要求
- 支持键盘导航
- 提供适当的ARIA标签
- 确保颜色对比度符合标准
- 支持屏幕阅读器

### 5. 国际化支持
- 使用react-i18next进行国际化
- 提取所有文本到语言文件
- 支持RTL语言布局
- 提供语言切换功能

## 开发工具配置

### 1. VS Code配置
```json
// .vscode/settings.json
{
  "typescript.preferences.importModuleSpecifier": "relative",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "emmet.includeLanguages": {
    "typescript": "html"
  }
}
```

### 2. 推荐插件
- ES7+ React/Redux/React-Native snippets
- TypeScript Importer
- Auto Rename Tag
- Bracket Pair Colorizer
- GitLens

## 总结

本前端开发规范为项目管理Agent MVP提供了完整的开发指导，涵盖了从项目结构到代码质量的各个方面。遵循这些规范可以确保代码的一致性、可维护性和高质量，为项目的成功交付奠定坚实基础。

开发团队应该严格按照这些规范进行开发，并在项目过程中不断完善和优化规范内容。
