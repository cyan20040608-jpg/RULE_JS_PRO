"""路由模块导出入口。"""

from app.routers import admin, auth, crud

__all__ = ["auth", "admin", "crud"]
