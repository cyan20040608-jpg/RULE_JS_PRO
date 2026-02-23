"""应用入口：创建应用实例并注册路由。"""

from fastapi import FastAPI

from app.core.exceptions import install_exception_handlers
from app.routers import admin, auth, crud


def create_app() -> FastAPI:
    """创建并配置应用实例。"""
    app = FastAPI(title="Edu Cockpit API", version="1.0.0")

    # 注册全局异常处理，统一错误响应结构。
    install_exception_handlers(app)

    # 注册认证与管理员相关路由。
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
    app.include_router(crud.router, prefix="/api/crud", tags=["crud"])

    return app


app = create_app()
