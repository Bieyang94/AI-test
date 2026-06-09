
import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.service.server.config import get_settings
from app.service.server.logging_config import setup_logging
from app.service.server.router.upload import router as upload_router
from app.service.server.router.generate_outline_stream import router as outline_router
from app.service.server.router.generate_xmind_stream import router as xmind_router
from app.service.server.router.generate_csv import router as csv_router

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.LOG_LEVEL)
    logger.info("🚀 %s v%s 启动中 ...", settings.APP_NAME, settings.APP_VERSION)
    logger.info("缓存配置: max_entries=%d, ttl=%ds", settings.CACHE_MAX_ENTRIES, settings.CACHE_TTL_SECONDS)
    yield
    logger.info("🛑 %s 正在关闭 ...", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_trace_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    request.state.request_id = request_id
    start = time.perf_counter()

    response = await call_next(request)

    elapsed = time.perf_counter() - start
    logger.info(
        "[%s] %s %s → %d (%.2fs)",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.3f}"
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "request_id": getattr(request.state, "request_id", None),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "请求参数校验失败",
            "details": exc.errors(),
            "request_id": getattr(request.state, "request_id", None),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("未捕获异常: %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": "服务内部错误",
            "request_id": getattr(request.state, "request_id", None),
        },
    )


app.include_router(upload_router)
app.include_router(outline_router)
app.include_router(xmind_router)
app.include_router(csv_router)


@app.get("/", tags=["系统"])
async def root():
    return {"service": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/health", tags=["系统"])
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.service.server.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
