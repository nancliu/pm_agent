"""
项目管理 Agent 主应用模块
"""

from fastapi import FastAPI
from config import settings
from database import init_db
from routes import router as task_router
from auth_routes import router as auth_router

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于OpenWebUI的科研项目管理智能应用",
    debug=settings.DEBUG
)

# 注册路由
app.include_router(task_router, prefix="/api/pm_agent")
app.include_router(auth_router, prefix="/api/pm_agent")

# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库连接"""
    await init_db()

# 应用关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理资源"""
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
