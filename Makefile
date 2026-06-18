# Makefile لمشروع Nexus

.PHONY: help install run test clean docker-build docker-up docker-down

help:
	@echo "أوامر مشروع Nexus"
	@echo "=================="
	@echo "make install       - تثبيت المتطلبات"
	@echo "make run           - تشغيل الخادم"
	@echo "make test          - تشغيل الاختبارات"
	@echo "make clean         - تنظيف المشروع"
	@echo "make docker-build  - بناء صور Docker"
	@echo "make docker-up     - تشغيل Docker"
	@echo "make docker-down   - إيقاف Docker"

install:
	@echo "📦 تثبيت المتطلبات..."
	pip install -r requirements.txt

run:
	@echo "🚀 تشغيل الخادم..."
	python -m backend.main

test:
	@echo "🧪 تشغيل الاختبارات..."
	pytest tests/ -v --cov=backend

clean:
	@echo "🧹 تنظيف المشروع..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".coverage" -delete

docker-build:
	@echo "🐳 بناء صور Docker..."
	docker-compose build

docker-up:
	@echo "🚀 تشغيل Docker..."
	docker-compose up -d

docker-down:
	@echo "🛑 إيقاف Docker..."
	docker-compose down

docker-logs:
	@echo "📋 عرض سجلات Docker..."
	docker-compose logs -f

lint:
	@echo "🔍 فحص الكود..."
	flake8 backend/
	black --check backend/

format:
	@echo "✨ تنسيق الكود..."
	black backend/
	isort backend/

requirements-upgrade:
	@echo "📦 تحديث المتطلبات..."
	pip install --upgrade -r requirements.txt
