"""
🤖 نظام محادثة ذكي
Chat Engine - Intelligent conversation system
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """أنواع الرسائل"""
    TEXT = "text"
    COMMAND = "command"
    CODE = "code"
    FILE = "file"
    IMAGE = "image"
    AUDIO = "audio"


class ConversationMessage:
    """رسالة محادثة"""
    
    def __init__(
        self,
        content: str,
        sender: str,
        message_type: MessageType = MessageType.TEXT,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.content = content
        self.sender = sender
        self.message_type = message_type
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل الرسالة لقاموس"""
        return {
            "content": self.content,
            "sender": self.sender,
            "type": self.message_type.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class Conversation:
    """محادثة كاملة"""
    
    def __init__(self, conversation_id: str, user_id: str, title: str = "Untitled"):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.title = title
        self.messages: List[ConversationMessage] = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def add_message(self, message: ConversationMessage) -> None:
        """إضافة رسالة للمحادثة"""
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
        logger.info(f"Message added to conversation {self.conversation_id}")
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """الحصول على سجل المحادثة"""
        messages = self.messages if limit is None else self.messages[-limit:]
        return [msg.to_dict() for msg in messages]
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل المحادثة لقاموس"""
        return {
            "id": self.conversation_id,
            "user_id": self.user_id,
            "title": self.title,
            "message_count": len(self.messages),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "messages": self.get_history()
        }


class ChatEngine:
    """محرك المحادثات الذكي"""
    
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.command_handlers: Dict[str, Any] = {}
        logger.info("ChatEngine initialized")
    
    def create_conversation(
        self, 
        user_id: str, 
        conversation_id: str,
        title: str = "Untitled"
    ) -> Conversation:
        """إنشاء محادثة جديدة"""
        conversation = Conversation(conversation_id, user_id, title)
        self.conversations[conversation_id] = conversation
        logger.info(f"Conversation created: {conversation_id} for user: {user_id}")
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """الحصول على محادثة"""
        return self.conversations.get(conversation_id)
    
    def process_message(
        self,
        conversation_id: str,
        content: str,
        sender: str,
        message_type: MessageType = MessageType.TEXT
    ) -> Dict[str, Any]:
        """معالجة رسالة جديدة"""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return {"error": "Conversation not found"}
        
        # إضافة الرسالة المستقبلة
        user_message = ConversationMessage(content, sender, message_type)
        conversation.add_message(user_message)
        
        # معالجة الرسالة
        response = self._process_content(content, message_type)
        
        # إضافة رسالة الرد
        bot_message = ConversationMessage(
            response["content"],
            "system",
            MessageType.TEXT,
            metadata=response.get("metadata", {})
        )
        conversation.add_message(bot_message)
        
        return response
    
    def _process_content(self, content: str, message_type: MessageType) -> Dict[str, Any]:
        """معالجة محتوى الرسالة"""
        if message_type == MessageType.COMMAND:
            return self._handle_command(content)
        elif message_type == MessageType.CODE:
            return self._handle_code(content)
        else:
            return self._handle_text(content)
    
    def _handle_text(self, content: str) -> Dict[str, Any]:
        """معالجة النص"""
        # هنا سيتم الاتصال بـ OpenAI API
        return {
            "content": f"تم استقبال رسالتك: {content}",
            "type": MessageType.TEXT.value,
            "metadata": {}
        }
    
    def _handle_command(self, content: str) -> Dict[str, Any]:
        """معالجة الأوامر"""
        command = content.split()[0] if content else ""
        
        if command == "/help":
            return {
                "content": "الأوامر المتاحة: /help, /status, /create_project",
                "type": MessageType.TEXT.value
            }
        elif command == "/status":
            return {
                "content": "النظام يعمل بشكل طبيعي",
                "type": MessageType.TEXT.value
            }
        else:
            return {
                "content": f"أمر غير معروف: {command}",
                "type": MessageType.TEXT.value
            }
    
    def _handle_code(self, content: str) -> Dict[str, Any]:
        """معالجة الأكواد"""
        return {
            "content": f"تم استقبال الكود وتم تحليله",
            "type": MessageType.CODE.value,
            "metadata": {"language": "python"}
        }
    
    def register_command_handler(self, command: str, handler) -> None:
        """تسجيل معالج أمر جديد"""
        self.command_handlers[command] = handler
        logger.info(f"Command handler registered: {command}")
    
    def list_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        """الحصول على قائمة المحادثات للمستخدم"""
        user_conversations = [
            conv for conv in self.conversations.values()
            if conv.user_id == user_id
        ]
        return [conv.to_dict() for conv in user_conversations]


# مثيل عام من محرك المحادثات
chat_engine = ChatEngine()
