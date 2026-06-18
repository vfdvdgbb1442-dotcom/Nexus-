# دليل البدء السريع

## المتطلبات
- Python 3.9 أو أحدث
- Docker و Docker Compose (اختياري)

## التثبيت

### 1. استنساخ المشروع
```bash
git clone https://github.com/vfdvdgbb1442-dotcom/Nexus.git
cd Nexus
```

### 2. إنشاء بيئة افتراضية
```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
venv\Scripts\activate     # على Windows
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. إعداد ملف البيئة
```bash
cp .env.example .env
# قم بتعديل .env وأضف بيانات حساسة
```

### 5. تشغيل الخادم
```bash
python -m backend.main
```

الخادم سيعمل على: `http://localhost:8000`

## استخدام Docker

```bash
# بناء الصور
docker-compose build

# تشغيل الخدمات
docker-compose up

# إيقاف الخدمات
docker-compose down
```

## الوصول للتطبيق

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Frontend**: http://localhost:3000 (بعد تشغيل frontend)

## الهيكل الأساسي

```
Nexus/
├── backend/           # النواة الأساسية
│   ├── core/         # المكونات الأساسية
│   ├── agents/       # الوكلاء
│   ├── services/     # الخدمات
│   ├── database/     # قاعدة البيانات
│   ├── api/          # API المسارات
│   └── main.py       # التطبيق الرئيسي
├── frontend/         # الواجهات
├── config/           # الإعدادات
├── docs/             # التوثيق
└── tests/            # الاختبارات
```

## المزايا الرئيسية

✅ نظام محادثة ذكي
✅ نظام ذاكرة متقدم
✅ وكلاء متعددة ومتخصصة
✅ إدارة مشاريع متكاملة
✅ نظام مراقبة شامل
✅ قابلية التوسع العالية

## الخطوات التالية

1. إعداد قاعدة البيانات
2. تثبيت مفاتيح API الخارجية
3. تشغيل الاختبارات
4. نشر التطبيق

## الدعم والمساعدة

للاستفسارات والدعم: support@nexus.ai
