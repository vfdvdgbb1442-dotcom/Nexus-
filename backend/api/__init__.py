"""
🌐 مسارات API الرئيسية
API Routes - Main API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.database import get_db
from backend.services import UserService
from backend.core.chat_engine import chat_engine, MessageType

router = APIRouter(prefix="/api/v1", tags=["api"])


# ==================== مسارات المحادثات ====================

@router.post("/conversations/create")
def create_conversation(
    user_id: str,
    title: str = "Untitled",
    db: Session = Depends(get_db)
):
    """إنشاء محادثة جديدة"""
    try:
        conversation_id = f"conv_{user_id}_{hash(title)}"
        conversation = chat_engine.create_conversation(user_id, conversation_id, title)
        return {
            "status": "success",
            "data": conversation.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations/{conversation_id}/message")
def send_message(
    conversation_id: str,
    content: str,
    sender: str,
    message_type: str = "text",
    db: Session = Depends(get_db)
):
    """إرسال رسالة في محادثة"""
    try:
        msg_type = MessageType(message_type)
        result = chat_engine.process_message(
            conversation_id,
            content,
            sender,
            msg_type
        )
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    """الحصول على محادثة"""
    try:
        conversation = chat_engine.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "status": "success",
            "data": conversation.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/user/{user_id}")
def list_user_conversations(user_id: str):
    """الحصول على قائمة محادثات المستخدم"""
    try:
        conversations = chat_engine.list_conversations(user_id)
        return {
            "status": "success",
            "data": conversations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== مسارات الوكلاء ====================

@router.get("/agents")
def list_agents():
    """الحصول على قائمة جميع الوكلاء"""
    try:
        from backend.core.agent_orchestrator import agent_orchestrator
        agents = agent_orchestrator.list_agents()
        return {
            "status": "success",
            "data": agents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/{agent_id}")
def get_agent(agent_id: str):
    """الحصول على وكيل محدد"""
    try:
        from backend.core.agent_orchestrator import agent_orchestrator
        agent = agent_orchestrator.get_agent(agent_id)
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return {
            "status": "success",
            "data": agent.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/execute")
def execute_task(agent_id: str, task: Dict[str, Any]):
    """تنفيذ مهمة من قبل وكيل"""
    try:
        from backend.core.agent_orchestrator import agent_orchestrator
        result = agent_orchestrator.execute_task(agent_id, task)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== مسارات الذاكرة ====================

@router.post("/memory/save")
def save_memory(
    entry_id: str,
    memory_type: str,
    content: Dict[str, Any],
    user_id: str,
    tags: List[str] = None,
    priority: int = 1
):
    """حفظ مدخل ذاكرة جديد"""
    try:
        from backend.core.memory_manager import memory_manager, MemoryType
        
        mem_type = MemoryType(memory_type)
        entry = memory_manager.save_memory(
            entry_id,
            mem_type,
            content,
            user_id,
            tags,
            priority
        )
        
        return {
            "status": "success",
            "data": entry.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memory/{entry_id}")
def get_memory(entry_id: str):
    """الحصول على مدخل ذاكرة"""
    try:
        from backend.core.memory_manager import memory_manager
        
        entry = memory_manager.get_memory(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Memory entry not found")
        
        return {
            "status": "success",
            "data": entry.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memory/user/{user_id}")
def get_user_memories(user_id: str, memory_type: str = None, limit: int = 10):
    """الحصول على ذاكرات المستخدم"""
    try:
        from backend.core.memory_manager import memory_manager, MemoryType
        
        mem_type = MemoryType(memory_type) if memory_type else None
        memories = memory_manager.get_user_memories(user_id, mem_type, limit)
        
        return {
            "status": "success",
            "data": [m.to_dict() for m in memories]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== مسارات الصحة ====================

@router.get("/health")
def health_check():
    """فحص صحة الخادم"""
    return {
        "status": "healthy",
        "service": "Nexus API v1"
    }
