.PHONY: dev test migrate seed clean

# Development
up:
	docker-compose up -d

down:
	docker-compose down

dev: up
	@echo "✅ Backend dev stack started. Access API at http://localhost:8000"

# Database
migrate:
	@echo "🚀 Running migrations..."
	alembic upgrade head

seed:
	@echo "🌱 Seeding database..."
	python seed.py

# Testing
test:
	@echo "🧪 Running tests..."
	pytest -v tests/

# Clean
clean:
	docker-compose down -v
	@echo "🧹 Cleaned up containers and volumes"

.PHONY: up down dev migrate seed test clean
