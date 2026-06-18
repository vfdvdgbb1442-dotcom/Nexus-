"""
📝 نظام التسجيل والتتبع
Logging Configuration
"""

import logging
import logging.handlers
import os
from pathlib import Path
from config.settings import get_settings

# الحصول على الإعدادات
settings = get_settings()

# إنشاء مجلد السجلات
log_dir = Path(settings.log_file).parent
log_dir.mkdir(parents=True, exist_ok=True)

# إعداد معالج التسجيل
def setup_logging():
    """إعداد نظام التسجيل"""
    
    # إنشاء المسجل الجذري
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))
    
    # معالج الملف
    file_handler = logging.handlers.RotatingFileHandler(
        settings.log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # معالج الكونسول
    console_handler = logging.StreamHandler()
    
    # صيغة التسجيل
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # تطبيق الصيغة على المعالجات
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # إضافة المعالجات
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # تعطيل سجلات المكتبات المحتفة
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# استدعاء الإعداد عند الاستيراد
setup_logging()
