"""
⚙️ إعدادات التطبيق الرئيسية
Configuration settings for Nexus Platform
"""

from typing import Optional, List
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """إعدادات التطبيق الرئيسية"""
    
    # Application
    app_name: str = "Nexus"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    api_prefix: str = "/api/v1"
    
    # Database
    db_type: str = "postgresql"  # postgresql or mongodb
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "nexus_db"
    db_user: str = "nexus_user"
    db_password: str = "nexus_password"
    
    # MongoDB (optional)
    mongo_uri: Optional[str] = "mongodb://localhost:27017"
    
    # Redis Cache
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # OpenAI API
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # External Services
    github_token: Optional[str] = None
    gitlab_token: Optional[str] = None
    
    # File Storage
    upload_dir: str = "./uploads"
    max_upload_size: int = 104857600  # 100MB
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Logging
    log_file: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """Get database URL"""
        if self.db_type == "postgresql":
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        return f"sqlite:///./test.db"
    
    @property
    def redis_url(self) -> str:
        """Get Redis URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


@lru_cache()
def get_settings() -> Settings:
    """الحصول على إعدادات التطبيق"""
    return Settings()
