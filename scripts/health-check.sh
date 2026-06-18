#!/bin/bash
# سكريبت فحص صحة النظام

echo "🔍 فحص صحة نظام Nexus"
echo "===================="

# فحص Python
echo ""
echo "✓ فحص Python..."
python --version

# فحص المتطلبات
echo ""
echo "✓ فحص المتطلبات..."
pip list | grep -E "fastapi|sqlalchemy|uvicorn" || echo "تحذير: بعض المتطلبات غير مثبتة"

# فحص الملفات الأساسية
echo ""
echo "✓ فحص الملفات الأساسية..."
required_files=(
    "backend/main.py"
    "backend/core/chat_engine.py"
    "backend/core/memory_manager.py"
    "backend/core/agent_orchestrator.py"
    "backend/database/models.py"
    "requirements.txt"
    ".env.example"
    "docker-compose.yml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file مفقود!"
    fi
done

# فحص المجلدات
echo ""
echo "✓ فحص المجلدات..."
required_dirs=(
    "backend"
    "backend/core"
    "backend/agents"
    "backend/services"
    "backend/database"
    "backend/api"
    "frontend"
    "docs"
    "tests"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    else
        echo "  ✗ $dir مفقود!"
    fi
done

# فحص قاعدة البيانات
echo ""
echo "✓ فحص قاعدة البيانات..."
if command -v psql &> /dev/null; then
    echo "  ✓ PostgreSQL مثبت"
else
    echo "  ⚠ PostgreSQL غير مثبت (اختياري إذا استخدمت SQLite)"
fi

# فحص Docker
echo ""
echo "✓ فحص Docker..."
if command -v docker &> /dev/null; then
    echo "  ✓ Docker مثبت"
    docker --version
else
    echo "  ⚠ Docker غير مثبت (اختياري)"
fi

echo ""
echo "✅ انتهى الفحص!"
echo "للبدء: python -m backend.main"
