# مرجع API

## نقاط النهاية الرئيسية

### المحادثات

#### إنشاء محادثة
```
POST /api/v1/conversations/create

Body:
{
  "user_id": "user_123",
  "title": "مشروع جديد"
}

Response:
{
  "status": "success",
  "data": {
    "id": "conv_123",
    "user_id": "user_123",
    "title": "مشروع جديد",
    "created_at": "2024-01-01T10:00:00"
  }
}
```

#### إرسال رسالة
```
POST /api/v1/conversations/{conversation_id}/message

Body:
{
  "content": "محتوى الرسالة",
  "sender": "user",
  "message_type": "text"
}

Response:
{
  "status": "success",
  "data": {
    "content": "رد النظام",
    "type": "text"
  }
}
```

#### الحصول على محادثة
```
GET /api/v1/conversations/{conversation_id}

Response:
{
  "status": "success",
  "data": {
    "id": "conv_123",
    "messages": [...],
    "created_at": "2024-01-01T10:00:00"
  }
}
```

#### الحصول على قائمة المحادثات
```
GET /api/v1/conversations/user/{user_id}

Response:
{
  "status": "success",
  "data": [
    {
      "id": "conv_123",
      "title": "محادثة 1"
    },
    {
      "id": "conv_124",
      "title": "محادثة 2"
    }
  ]
}
```

### الوكلاء

#### الحصول على قائمة الوكلاء
```
GET /api/v1/agents

Response:
{
  "status": "success",
  "data": [
    {
      "id": "agent_chat_001",
      "type": "chat",
      "name": "Chat Assistant",
      "is_active": true
    },
    {
      "id": "agent_code_001",
      "type": "code",
      "name": "Code Developer"
    }
  ]
}
```

#### الحصول على وكيل معين
```
GET /api/v1/agents/{agent_id}

Response:
{
  "status": "success",
  "data": {
    "id": "agent_code_001",
    "type": "code",
    "name": "Code Developer",
    "stats": {
      "tasks_completed": 10,
      "tasks_failed": 1
    }
  }
}
```

#### تنفيذ مهمة
```
POST /api/v1/agents/{agent_id}/execute

Body:
{
  "action": "create",
  "language": "python",
  "description": "دالة لحساب المضروب"
}

Response:
{
  "status": "success",
  "data": {
    "result": "كود تم إنشاؤه"
  }
}
```

### الذاكرة

#### حفظ مدخل ذاكرة
```
POST /api/v1/memory/save

Body:
{
  "entry_id": "mem_123",
  "memory_type": "project",
  "content": {
    "name": "مشروع جديد",
    "description": "وصف المشروع"
  },
  "user_id": "user_123",
  "tags": ["important"],
  "priority": 3
}

Response:
{
  "status": "success",
  "data": {
    "id": "mem_123",
    "type": "project"
  }
}
```

#### الحصول على مدخل ذاكرة
```
GET /api/v1/memory/{entry_id}

Response:
{
  "status": "success",
  "data": {
    "id": "mem_123",
    "type": "project",
    "content": {...}
  }
}
```

#### الحصول على ذاكرات المستخدم
```
GET /api/v1/memory/user/{user_id}?memory_type=project&limit=10

Response:
{
  "status": "success",
  "data": [
    {
      "id": "mem_123",
      "type": "project",
      "content": {...}
    }
  ]
}
```

### الصحة والحالة

#### فحص صحة الخادم
```
GET /api/v1/health

Response:
{
  "status": "healthy",
  "service": "Nexus API v1"
}
```

#### حالة التطبيق
```
GET /status

Response:
{
  "status": "healthy",
  "app_name": "Nexus",
  "version": "1.0.0"
}
```

## رموز الأخطاء

| الكود | المعنى | الحل |
|------|--------|------|
| 200 | نجاح | - |
| 400 | طلب سيء | تحقق من البيانات المرسلة |
| 401 | غير مصرح | سجل دخولك أولاً |
| 404 | غير موجود | تحقق من المعرف |
| 500 | خطأ في الخادم | حاول لاحقاً |

## مثال شامل

```bash
# 1. إنشاء محادثة
curl -X POST http://localhost:8000/api/v1/conversations/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "title": "حل مسألة برمجية"
  }'

# 2. إرسال رسالة
curl -X POST http://localhost:8000/api/v1/conversations/conv_123/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": "أريد دالة لحساب المضروب",
    "sender": "user",
    "message_type": "text"
  }'

# 3. الحصول على قائمة الوكلاء
curl http://localhost:8000/api/v1/agents

# 4. تنفيذ مهمة برمجية
curl -X POST http://localhost:8000/api/v1/agents/agent_code_001/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create",
    "language": "python"
  }'
```
