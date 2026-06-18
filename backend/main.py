"""
🚀 تطبيق Nexus الرئيسي
Main Application Entry Point
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from contextlib import asynccontextmanager

from config.settings import get_settings
from backend.logging_config import setup_logging
from backend.database import init_db, close_db
from backend.api import router as api_router

# إعداد التسجيل
setup_logging()
logger = logging.getLogger(__name__)

# الحصول على الإعدادات
settings = get_settings()


# دورة حياة التطبيق
@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة حياة التطبيق"""
    # البدء
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    yield
    
    # الإيقاف
    logger.info(f"Shutting down {settings.app_name}")
    close_db()


# إنشاء تطبيق FastAPI
app = FastAPI(
    title=settings.app_name,
    description="منصة ذكاء اصطناعي متكاملة وقابلة للتوسع",
    version=settings.app_version,
    lifespan=lifespan
)

# إضافة Middleware
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# تسجيل المسارات
app.include_router(api_router)


# مسارات إضافية
@app.get("/")
def root():
    """المسار الجذري"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "api_prefix": settings.api_prefix
    }


@app.get("/status")
def status():
    """حالة التطبيق"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }


@app.get("/config")
def get_config():
    """الحصول على الإعدادات العامة (بدون بيانات حساسة)"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "api_prefix": settings.api_prefix,
        "database_type": settings.db_type
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
