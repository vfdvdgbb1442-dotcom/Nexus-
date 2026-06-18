# دليل المطورين

## بيئة التطوير

### المتطلبات
- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Node.js 16+ (للواجهة الأمامية)

### الإعداد الأولي

```bash
# استنساخ المشروع
git clone https://github.com/vfdvdgbb1442-dotcom/Nexus.git
cd Nexus

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt

# إعداد البيئة
cp .env.example .env
# تحرير .env بمعلوماتك

# تشغيل الخادم
python -m backend.main
```

## هيكل المشروع

```
backend/
├── core/
│   ├── __init__.py
│   ├── chat_engine.py      # محرك المحادثات
│   ├── memory_manager.py   # مدير الذاكرة
│   └── agent_orchestrator.py  # منسق الوكلاء
├── agents/                 # الوكلاء المتخصصة
├── services/              # الخدمات الأساسية
├── database/              # نماذج قاعدة البيانات
├── api/                   # مسارات API
└── main.py               # نقطة الدخول الرئيسية
```

## مراحل التطوير

### المرحلة 1: النواة الأساسية ✅
- [x] هيكل المشروع
- [x] إعدادات النظام
- [x] محرك المحادثات
- [x] مدير الذاكرة
- [x] منسق الوكلاء

### المرحلة 2: قاعدة البيانات (جاري)
- [ ] تكامل قاعدة البيانات الكاملة
- [ ] نماذج إضافية
- [ ] Migrations

### المرحلة 3: الوكلاء المتقدمة
- [ ] وكيل البرمجة المتقدمة
- [ ] وكيل منشئ المواقع
- [ ] وكيل تطوير التطبيقات
- [ ] وكيل الألعاب

### المرحلة 4: الواجهة الأمامية
- [ ] تطبيق الويب (React)
- [ ] تطبيق الجوال (React Native)

### المرحلة 5: الميزات المتقدمة
- [ ] نظام الموافقات
- [ ] نظام المراقبة الشامل
- [ ] نظام التحسين الذاتي

## معايير الكود

### تسمية المتغيرات
```python
# ✅ جيد
user_conversations = []
max_retries = 3
is_active = True

# ❌ سيء
uc = []
mr = 3
active = True
```

### التعليقات والتوثيق
```python
def process_message(content: str, sender: str) -> Dict[str, Any]:
    """
    معالجة رسالة جديدة
    
    Args:
        content: محتوى الرسالة
        sender: مرسل الرسالة
        
    Returns:
        قاموس بنتيجة المعالجة
    """
```

### Type Hints
```python
from typing import Optional, List, Dict, Any

def get_user(user_id: str) -> Optional[User]:
    ...

def list_conversations(user_id: str) -> List[Conversation]:
    ...
```

## الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest

# تشغيل اختبارات معينة
pytest tests/test_chat_engine.py

# عرض التغطية
pytest --cov=backend tests/
```

## Git Workflow

```bash
# إنشاء فرع جديد
git checkout -b feature/my-feature

# الإرسال والالتزام
git add .
git commit -m "feat: description of changes"

# دفع الفرع
git push origin feature/my-feature

# طلب دمج (Pull Request)
# اذهب للموقع وأنشئ PR
```

## الترجيح المرتقب

- [ ] دعم اللغات المتعددة
- [ ] نشر على AWS/Google Cloud
- [ ] دعم OpenAI API المتقدم
- [ ] نظام الإشعارات الفورية
- [ ] تطبيق جوال أصلي

## الموارد المفيدة

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Python Best Practices](https://pep8.org/)
- [REST API Design](https://restfulapi.net/)
