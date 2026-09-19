.PHONY: install install-dev db-up db-down db-logs db-migrate init-db seed report-fraud report-text report-image report-ts report-multi test lint format clean version

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

db-up:
	docker compose up -d db

db-down:
	docker compose down

db-logs:
	docker compose logs -f db

db-migrate:
	@if [ -z "$(CMRE_DATABASE_URL)" ]; then \
		echo "CMRE_DATABASE_URL not set; using docker compose exec"; \
		docker compose exec -T db psql -U cmre -d cmre -f /dev/stdin < db_migrations/0001_pgvector.sql; \
	else \
		psql "$(CMRE_DATABASE_URL)" -f db_migrations/0001_pgvector.sql; \
	fi

init-db:
	cmre init-db

seed:
	cmre seed

report-fraud:
	cmre report --input data/examples/competition_fraud.json --output reports/fraud.md

report-text:
	cmre report --input data/examples/competition_text_classification.json --output reports/text.md

report-image:
	cmre report --input data/examples/competition_image_detection.json --output reports/image.md

report-ts:
	cmre report --input data/examples/competition_time_series_forecast.json --output reports/time_series.md

report-multi:
	cmre report --input data/examples/competition_multimodal.json --output reports/multimodal.md

report-all: report-fraud report-text report-image report-ts report-multi

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build *.egg-info
	find . -name '__pycache__' -type d -exec rm -rf {} +

version:
	cmre version
