PHONY: isort
isort:
	isort .
.PHONY: isortcheck
isortcheck:
	@echo "Checking isort..."
	isort --diff --check-only .

.PHONY: black
black:
	black .

.PHONY: blackcheck
blackcheck:
	@echo "Checking black..."
	black --check .

.PHONY: pyformatcheck
pyformatcheck: isortcheck blackcheck

.PHONY: mypy
mypy:
	@echo "Checking mypy..."
	mypy .

.PHONY: lint
lint: pyformatcheck mypy

.PHONY: autofmt
autofmt: pyformatcheck
	@echo "Formatting code..."
	isort .
	black .

.PHONY: rebuilddb
rebuilddb:
	@echo "Rebuild container"
	docker-compose build
	@echo "Finish"

.PHONY: startdb
startdb:
	@echo "Starting MongoDB container..."
	@echo "Data will be stored in ./data"
	docker-compose up -d

.PHONY: setupdb
setupdb:
	@echo "Setting up database..."
	docker-compose build

.PHONY: stopdb
stopdb:
	@echo "Stopping Mongo container..."
	docker-compose down