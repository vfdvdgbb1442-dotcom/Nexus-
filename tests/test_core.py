"""
اختبارات المشروع
Test Suite for Nexus Platform
"""

import pytest
import sys
from pathlib import Path

# إضافة المسار للمشروع
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestChatEngine:
    """اختبارات محرك المحادثات"""
    
    def test_create_conversation(self):
        """اختبار إنشاء محادثة"""
        from backend.core.chat_engine import chat_engine
        
        conversation = chat_engine.create_conversation(
            "user_123",
            "conv_123",
            "Test Conversation"
        )
        
        assert conversation is not None
        assert conversation.user_id == "user_123"
        assert conversation.title == "Test Conversation"
    
    def test_process_message(self):
        """اختبار معالجة رسالة"""
        from backend.core.chat_engine import chat_engine
        
        conversation = chat_engine.create_conversation("user_123", "conv_123")
        result = chat_engine.process_message(
            "conv_123",
            "مرحبا",
            "user",
        )
        
        assert result is not None
        assert result.get("status") in ["success", "error"]


class TestMemoryManager:
    """اختبارات مدير الذاكرة"""
    
    def test_save_memory(self):
        """اختبار حفظ الذاكرة"""
        from backend.core.memory_manager import memory_manager, MemoryType
        
        entry = memory_manager.save_memory(
            "mem_123",
            MemoryType.PROJECT,
            {"name": "test_project"},
            "user_123"
        )
        
        assert entry is not None
        assert entry.entry_id == "mem_123"
    
    def test_get_memory(self):
        """اختبار الحصول على الذاكرة"""
        from backend.core.memory_manager import memory_manager, MemoryType
        
        memory_manager.save_memory(
            "mem_123",
            MemoryType.PROJECT,
            {"name": "test"},
            "user_123"
        )
        
        entry = memory_manager.get_memory("mem_123")
        assert entry is not None


class TestAgentOrchestrator:
    """اختبارات منسق الوكلاء"""
    
    def test_list_agents(self):
        """اختبار الحصول على قائمة الوكلاء"""
        from backend.core.agent_orchestrator import agent_orchestrator
        
        agents = agent_orchestrator.list_agents()
        assert len(agents) > 0
    
    def test_execute_task(self):
        """اختبار تنفيذ مهمة"""
        from backend.core.agent_orchestrator import agent_orchestrator
        
        result = agent_orchestrator.execute_task(
            "agent_chat_001",
            {"message": "test"}
        )
        
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
