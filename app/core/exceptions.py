"""全局异常处理：输出统一错误格式。"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.response import error_response


def install_exception_handlers(app: FastAPI) -> None:
    """注册全局异常处理器。"""

    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
        message = exc.detail if isinstance(exc.detail, str) else "请求失败"
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.status_code, message),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_response(422, "请求参数校验失败", exc.errors()),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=error_response(500, f"服务器内部错误: {exc}"),
        )
