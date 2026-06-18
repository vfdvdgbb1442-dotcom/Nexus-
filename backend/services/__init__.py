"""
📋 خدمة إدارة المستخدمين
User Service - User management and authentication
"""

import logging
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.database.models import User

logger = logging.getLogger(__name__)

# تشفير كلمات المرور
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """خدمة إدارة المستخدمين"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """تشفير كلمة المرور"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """التحقق من كلمة المرور"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_user(
        db: Session,
        email: str,
        username: str,
        password: str,
        full_name: str
    ) -> Optional[User]:
        """إنشاء مستخدم جديد"""
        try:
            # التحقق من عدم وجود المستخدم بالفعل
            existing_user = db.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()
            
            if existing_user:
                logger.warning(f"User already exists: {email}")
                return None
            
            user = User(
                id=str(uuid.uuid4()),
                email=email,
                username=username,
                full_name=full_name,
                hashed_password=UserService.hash_password(password)
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info(f"User created: {email}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create user: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """الحصول على مستخدم من البريد الإلكتروني"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """الحصول على مستخدم من المعرف"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        """مصادقة المستخدم"""
        user = UserService.get_user_by_email(db, email)
        
        if not user:
            return None
        
        if not UserService.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user


class ConversationService:
    """خدمة إدارة المحادثات"""
    
    @staticmethod
    def create_conversation(
        db: Session,
        user_id: str,
        title: str = "Untitled",
        description: str = ""
    ) -> Optional:
        """إنشاء محادثة جديدة"""
        from backend.database.models import Conversation
        
        try:
            conversation = Conversation(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=title,
                description=description
            )
            
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
            logger.info(f"Conversation created: {conversation.id}")
            return conversation
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create conversation: {str(e)}")
            return None
    
    @staticmethod
    def get_user_conversations(db: Session, user_id: str):
        """الحصول على محادثات المستخدم"""
        from backend.database.models import Conversation
        
        return db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).all()


class ProjectService:
    """خدمة إدارة المشاريع"""
    
    @staticmethod
    def create_project(
        db: Session,
        user_id: str,
        name: str,
        description: str,
        project_type: str
    ) -> Optional:
        """إنشاء مشروع جديد"""
        from backend.database.models import Project
        
        try:
            project = Project(
                id=str(uuid.uuid4()),
                user_id=user_id,
                name=name,
                description=description,
                project_type=project_type
            )
            
            db.add(project)
            db.commit()
            db.refresh(project)
            
            logger.info(f"Project created: {project.id}")
            return project
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create project: {str(e)}")
            return None
    
    @staticmethod
    def get_user_projects(db: Session, user_id: str):
        """الحصول على مشاريع المستخدم"""
        from backend.database.models import Project
        
        return db.query(Project).filter(
            Project.user_id == user_id
        ).order_by(Project.updated_at.desc()).all()


class TaskService:
    """خدمة إدارة المهام"""
    
    @staticmethod
    def create_task(
        db: Session,
        user_id: str,
        project_id: str,
        title: str,
        description: str,
        priority: int = 1
    ) -> Optional:
        """إنشاء مهمة جديدة"""
        from backend.database.models import Task
        
        try:
            task = Task(
                id=str(uuid.uuid4()),
                user_id=user_id,
                project_id=project_id,
                title=title,
                description=description,
                priority=priority
            )
            
            db.add(task)
            db.commit()
            db.refresh(task)
            
            logger.info(f"Task created: {task.id}")
            return task
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create task: {str(e)}")
            return None
    
    @staticmethod
    def get_project_tasks(db: Session, project_id: str):
        """الحصول على مهام المشروع"""
        from backend.database.models import Task
        
        return db.query(Task).filter(
            Task.project_id == project_id
        ).order_by(Task.priority.desc()).all()
