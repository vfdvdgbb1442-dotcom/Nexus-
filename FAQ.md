# أسئلة شائعة

## التثبيت والإعداد

### كيف أثبت المشروع؟
```bash
git clone https://github.com/vfdvdgbb1442-dotcom/Nexus.git
cd Nexus
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m backend.main
```

### هل يمكنني استخدام Docker؟
نعم! استخدم:
```bash
docker-compose up
```

### ما هي متطلبات النظام الأدنى؟
- Python 3.9 أو أحدث
- 2GB RAM على الأقل
- PostgreSQL 12+ أو SQLite

## الاستخدام

### كيف أبدأ محادثة جديدة؟
```bash
curl -X POST http://localhost:8000/api/v1/conversations/create \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "title": "محادثة جديدة"}'
```

### كيف أضيف وكيل جديد؟
انظر [دليل إنشاء وكلاء جديدة](docs/creating-custom-agents.md)

### كيف أعدّل إعدادات التطبيق؟
عدّل ملف `.env` بناءً على `.env.example`

## التطوير

### أين أضيف ميزات جديدة؟
انظر [دليل المطورين](docs/developer-guide.md)

### كيف أشغل الاختبارات؟
```bash
pytest tests/
```

### كيف أصلح خطأ؟
1. ابحث في السجلات: `logs/app.log`
2. تحقق من قاعدة البيانات
3. شغّل الاختبارات للتحقق

## النشر

### كيف أنشر التطبيق؟
```bash
make docker-build
make docker-up
```

### هل يمكنني النشر على AWS؟
نعم! استخدم بناء Docker والتوثيق في AWS ECR

### كيف أراقب الأداء؟
استخدم Prometheus و Grafana (انظر الإعدادات)

## المشاكل الشائعة

### خطأ في الاتصال بقاعدة البيانات
تحقق من إعدادات `.env` و تأكد من تشغيل PostgreSQL

### الخادم بطيء جداً
- فعّل Redis للتخزين المؤقت
- استخدم Gunicorn بدلاً من Uvicorn
- قلل عدد الاتصالات بقاعدة البيانات

### لا يعمل Docker؟
```bash
docker-compose down
docker system prune
docker-compose build --no-cache
docker-compose up
```

## الدعم والمساعدة

### أين أطلب المساعدة؟
- 📧 البريد: support@nexus.ai
- 🐙 GitHub Issues: رفع مشكلة جديدة
- 💬 مجتمع المطورين: الانضمام للمجموعة

### كيف أبلغ عن خطأ؟
أنشئ issue على GitHub مع:
- وصف المشكلة بالتفصيل
- خطوات إعادة إنتاج المشكلة
- السجلات ذات الصلة
