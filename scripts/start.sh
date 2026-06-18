#!/bin/bash
# سكريبت بدء التشغيل الكامل

set -e

echo "🚀 بدء تشغيل منصة Nexus"
echo "========================="

# التحقق من البيئة الافتراضية
if [ ! -d "venv" ]; then
    echo "📦 إنشاء بيئة افتراضية..."
    python3 -m venv venv
fi

# تفعيل البيئة الافتراضية
echo "✅ تفعيل البيئة الافتراضية..."
source venv/bin/activate

# تثبيت المتطلبات
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 تثبيت المتطلبات..."
    pip install -r requirements.txt
fi

# التحقق من ملف البيئة
if [ ! -f ".env" ]; then
    echo "⚙️ إنشاء ملف البيئة..."
    cp .env.example .env
    echo "⚠️ يرجى تعديل .env بمعلومات قاعدة البيانات الخاصة بك"
fi

# إنشاء مجلدات السجلات
mkdir -p logs uploads

# تشغيل الخادم
echo "🌐 تشغيل خادم Nexus على http://localhost:8000"
python -m backend.main
