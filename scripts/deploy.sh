#!/bin/bash
# سكريبت النشر

echo "📦 نشر مشروع Nexus"
echo "=================="

# البناء
echo "🔨 بناء الصور..."
docker-compose build

# الاختبارات
echo "🧪 تشغيل الاختبارات..."
pytest tests/ --cov=backend

# النشر
echo "🚀 نشر التطبيق..."
docker-compose up -d

echo "✅ تم النشر بنجاح"
echo "📊 الخادم متوفر على: http://localhost:8000"
