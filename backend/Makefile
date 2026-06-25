.PHONY: dev test lint

device:
	@echo "Running development stack..."

dev:
	docker-compose up --build

lint:
	flake8 backend/app

test:
	pytest backend/app/tests -s -v
