"""
🗄️ إدارة قاعدة البيانات
Database Connection and Management
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from config.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

# إنشاء محرك قاعدة البيانات
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=3600
)

# إنشاء جلسة
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """الحصول على جلسة قاعدة البيانات"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """تهيئة قاعدة البيانات"""
    from backend.database.models import Base
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def close_db():
    """إغلاق قاعدة البيانات"""
    engine.dispose()
    logger.info("Database connection closed")
