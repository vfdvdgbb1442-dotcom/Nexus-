"""
📊 نماذج قاعدة البيانات
Database Models - SQLAlchemy ORM Models
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """نموذج المستخدم"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    conversations = relationship("Conversation", back_populates="user")
    projects = relationship("Project", back_populates="user")
    tasks = relationship("Task", back_populates="user")
    settings = relationship("UserSetting", back_populates="user")


class Conversation(Base):
    """نموذج المحادثة"""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    message_count = Column(Integer, default=0)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    """نموذج الرسالة"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    sender = Column(String)  # "user" or "assistant"
    content = Column(Text)
    message_type = Column(String, default="text")  # text, code, file, etc.
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # العلاقات
    conversation = relationship("Conversation", back_populates="messages")


class Project(Base):
    """نموذج المشروع"""
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    description = Column(Text)
    project_type = Column(String)  # web, app, game, etc.
    status = Column(String, default="planning")  # planning, development, testing, deployed
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    """نموذج المهمة"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    project_id = Column(String, ForeignKey("projects.id"))
    title = Column(String)
    description = Column(Text)
    status = Column(String, default="todo")  # todo, in_progress, done
    priority = Column(Integer, default=1)  # 1-5
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    user = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")


class UserSetting(Base):
    """نموذج إعدادات المستخدم"""
    __tablename__ = "user_settings"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    key = Column(String)
    value = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    user = relationship("User", back_populates="settings")


class ErrorLog(Base):
    """نموذج سجل الأخطاء"""
    __tablename__ = "error_logs"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    error_type = Column(String)
    error_message = Column(Text)
    error_traceback = Column(Text)
    context = Column(JSON, default={})
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
class SystemMonitor(Base):
    """نموذج مراقبة النظام"""
    __tablename__ = "system_monitors"
    
    id = Column(String, primary_key=True)
    target_type = Column(String)  # website, app, project
    target_id = Column(String)
    status = Column(String)  # online, offline, error
    last_check = Column(DateTime, default=datetime.utcnow)
    uptime_percentage = Column(Integer)
    error_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
