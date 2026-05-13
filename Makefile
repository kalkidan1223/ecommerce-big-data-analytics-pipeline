.PHONY: help setup install test run-pipeline run-airflow run-dbt clean docker-up docker-down

help:
	@echo "Data Pipeline Development Commands"
	@echo "===================================="
	@echo "make setup          - Setup virtual environment and install dependencies"
	@echo "make install        - Install Python dependencies"
	@echo "make test           - Run tests"
	@echo "make run-pipeline   - Run the complete ETL pipeline"
	@echo "make run-airflow    - Start Airflow scheduler and webserver"
	@echo "make run-dbt        - Run dbt models"
	@echo "make clean          - Clean up cache and temporary files"
	@echo "make docker-up      - Start Docker containers"
	@echo "make docker-down    - Stop Docker containers"

setup:
	@echo "Setting up virtual environment..."
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  On Windows: venv\\Scripts\\activate"
	@echo "  On Unix: source venv/bin/activate"
	$(MAKE) install

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "Dependencies installed successfully!"

test:
	@echo "Running tests..."
	pytest tests/ -v --cov=src

run-pipeline:
	@echo "Running ETL pipeline..."
	python -m src.pipeline

run-airflow:
	@echo "Starting Airflow..."
	@echo "Starting scheduler..."
	@echo "Note: Run in separate terminals:"
	@echo "  Terminal 1: export AIRFLOW_HOME=./airflow && airflow scheduler"
	@echo "  Terminal 2: export AIRFLOW_HOME=./airflow && airflow webserver --port 8080"
	@echo "Then access: http://localhost:8080"

run-dbt:
	@echo "Running dbt models..."
	cd dbt/analytics && dbt run
	cd dbt/analytics && dbt test

dbt-docs:
	@echo "Generating dbt documentation..."
	cd dbt/analytics && dbt docs generate
	@echo "Documentation available at: ./dbt/analytics/target/index.html"

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "target" -path "*/dbt/*" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete!"

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "Containers started. Access Airflow at http://localhost:8080"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down
	@echo "Containers stopped."

docker-logs:
	docker-compose logs -f

lint:
	@echo "Linting Python code..."
	flake8 src/ --max-line-length=120
	black --check src/

format:
	@echo "Formatting Python code..."
	black src/

requirements-freeze:
	pip freeze > requirements-frozen.txt
	@echo "Frozen requirements saved to requirements-frozen.txt"
