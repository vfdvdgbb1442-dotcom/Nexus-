"""
💾 نظام الذاكرة المتقدم
Memory Manager - Advanced memory and knowledge management system
"""

import logging
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class MemoryType(str, Enum):
    """أنواع الذاكرة"""
    CONVERSATION = "conversation"
    PROJECT = "project"
    TASK = "task"
    USER_SETTING = "user_setting"
    KNOWLEDGE = "knowledge"
    ERROR_LOG = "error_log"


class MemoryEntry:
    """مدخل ذاكرة واحد"""
    
    def __init__(
        self,
        entry_id: str,
        memory_type: MemoryType,
        content: Dict[str, Any],
        user_id: str,
        tags: Optional[List[str]] = None,
        priority: int = 1
    ):
        self.entry_id = entry_id
        self.memory_type = memory_type
        self.content = content
        self.user_id = user_id
        self.tags = tags or []
        self.priority = priority
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.access_count = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل المدخل لقاموس"""
        return {
            "id": self.entry_id,
            "type": self.memory_type.value,
            "content": self.content,
            "user_id": self.user_id,
            "tags": self.tags,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "access_count": self.access_count
        }


class MemoryManager:
    """مدير الذاكرة المتقدم"""
    
    def __init__(self):
        self.memory_store: Dict[str, MemoryEntry] = {}
        self.user_memories: Dict[str, List[str]] = {}  # user_id -> [entry_ids]
        logger.info("MemoryManager initialized")
    
    def save_memory(
        self,
        entry_id: str,
        memory_type: MemoryType,
        content: Dict[str, Any],
        user_id: str,
        tags: Optional[List[str]] = None,
        priority: int = 1
    ) -> MemoryEntry:
        """حفظ مدخل ذاكرة جديد"""
        entry = MemoryEntry(entry_id, memory_type, content, user_id, tags, priority)
        self.memory_store[entry_id] = entry
        
        if user_id not in self.user_memories:
            self.user_memories[user_id] = []
        self.user_memories[user_id].append(entry_id)
        
        logger.info(f"Memory saved: {entry_id} for user: {user_id}")
        return entry
    
    def get_memory(self, entry_id: str) -> Optional[MemoryEntry]:
        """الحصول على مدخل ذاكرة"""
        entry = self.memory_store.get(entry_id)
        if entry:
            entry.access_count += 1
            entry.updated_at = datetime.utcnow()
        return entry
    
    def update_memory(
        self,
        entry_id: str,
        content: Dict[str, Any],
        tags: Optional[List[str]] = None
    ) -> Optional[MemoryEntry]:
        """تحديث مدخل ذاكرة"""
        entry = self.memory_store.get(entry_id)
        if entry:
            entry.content = content
            if tags:
                entry.tags = tags
            entry.updated_at = datetime.utcnow()
            logger.info(f"Memory updated: {entry_id}")
        return entry
    
    def delete_memory(self, entry_id: str) -> bool:
        """حذف مدخل ذاكرة"""
        if entry_id in self.memory_store:
            entry = self.memory_store.pop(entry_id)
            if entry.user_id in self.user_memories:
                self.user_memories[entry.user_id].remove(entry_id)
            logger.info(f"Memory deleted: {entry_id}")
            return True
        return False
    
    def search_memory(
        self,
        user_id: str,
        query: str,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None
    ) -> List[MemoryEntry]:
        """البحث عن مدخلات الذاكرة"""
        results = []
        
        if user_id not in self.user_memories:
            return results
        
        for entry_id in self.user_memories[user_id]:
            entry = self.memory_store.get(entry_id)
            if not entry:
                continue
            
            # تصفية حسب نوع الذاكرة
            if memory_type and entry.memory_type != memory_type:
                continue
            
            # تصفية حسب الوسوم
            if tags and not any(tag in entry.tags for tag in tags):
                continue
            
            # البحث في المحتوى
            query_lower = query.lower()
            content_str = json.dumps(entry.content).lower()
            
            if query_lower in content_str or query_lower in " ".join(entry.tags).lower():
                results.append(entry)
        
        # ترتيب النتائج حسب الأولوية والتاريخ
        results.sort(key=lambda x: (x.priority, x.updated_at), reverse=True)
        return results
    
    def get_user_memories(
        self,
        user_id: str,
        memory_type: Optional[MemoryType] = None,
        limit: Optional[int] = None
    ) -> List[MemoryEntry]:
        """الحصول على جميع ذاكرات المستخدم"""
        memories = []
        
        if user_id not in self.user_memories:
            return memories
        
        for entry_id in self.user_memories[user_id]:
            entry = self.memory_store.get(entry_id)
            if entry and (memory_type is None or entry.memory_type == memory_type):
                memories.append(entry)
        
        # ترتيب حسب التاريخ الأحدث أولاً
        memories.sort(key=lambda x: x.updated_at, reverse=True)
        
        if limit:
            memories = memories[:limit]
        
        return memories
    
    def save_conversation(
        self,
        conversation_id: str,
        user_id: str,
        conversation_data: Dict[str, Any]
    ) -> MemoryEntry:
        """حفظ سجل محادثة"""
        return self.save_memory(
            entry_id=f"conv_{conversation_id}",
            memory_type=MemoryType.CONVERSATION,
            content=conversation_data,
            user_id=user_id,
            tags=["conversation"],
            priority=2
        )
    
    def save_project(
        self,
        project_id: str,
        user_id: str,
        project_data: Dict[str, Any]
    ) -> MemoryEntry:
        """حفظ بيانات مشروع"""
        return self.save_memory(
            entry_id=f"proj_{project_id}",
            memory_type=MemoryType.PROJECT,
            content=project_data,
            user_id=user_id,
            tags=["project"],
            priority=3
        )
    
    def save_task(
        self,
        task_id: str,
        user_id: str,
        task_data: Dict[str, Any]
    ) -> MemoryEntry:
        """حفظ بيانات مهمة"""
        return self.save_memory(
            entry_id=f"task_{task_id}",
            memory_type=MemoryType.TASK,
            content=task_data,
            user_id=user_id,
            tags=["task"],
            priority=2
        )
    
    def save_error_log(
        self,
        error_id: str,
        user_id: str,
        error_data: Dict[str, Any]
    ) -> MemoryEntry:
        """حفظ سجل الخطأ"""
        return self.save_memory(
            entry_id=f"err_{error_id}",
            memory_type=MemoryType.ERROR_LOG,
            content=error_data,
            user_id=user_id,
            tags=["error"],
            priority=1
        )
    
    def get_statistics(self, user_id: str) -> Dict[str, Any]:
        """الحصول على إحصائيات الذاكرة"""
        memories = self.get_user_memories(user_id)
        
        type_counts = {}
        for entry in memories:
            mem_type = entry.memory_type.value
            type_counts[mem_type] = type_counts.get(mem_type, 0) + 1
        
        return {
            "total_entries": len(memories),
            "by_type": type_counts,
            "total_access_count": sum(m.access_count for m in memories),
            "latest_updated": max(
                (m.updated_at.isoformat() for m in memories),
                default=None
            )
        }


# مثيل عام من مدير الذاكرة
memory_manager = MemoryManager()
