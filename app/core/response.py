"""统一响应结构工具。"""

from typing import Any


def success_response(data: Any = None, message: str = "ok") -> dict[str, Any]:
    """构造统一成功响应。"""
    return {
        "code": 0,
        "message": message,
        "data": data,
    }


def error_response(code: int, message: str, data: Any = None) -> dict[str, Any]:
    """构造统一错误响应。"""
    return {
        "code": code,
        "message": message,
        "data": data,
    }
