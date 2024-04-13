run-migration:
	python -m app.infra.database.migration_runner.migration_runner

run-tests:
	poetry run pytest --cov-config=.coveragerc --cov-report html --cov=. ./tests