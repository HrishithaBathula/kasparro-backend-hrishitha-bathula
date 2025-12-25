.PHONY: up down restart logs build test etl normalize csv psql

up:
	docker compose up --build

down:
	docker compose down

restart:
	docker compose down
	docker compose up --build

logs:
	docker compose logs -f

build:
	docker compose build

etl:
	docker exec -it kasparro-backend-hrishitha-bathula-api-1 python -m ingestion.run_etl

normalize:
	docker exec -it kasparro-backend-hrishitha-bathula-api-1 python -m ingestion.normalize_coinpaprika

csv:
	docker exec -it kasparro-backend-hrishitha-bathula-api-1 python -m ingestion.csv_ingest

psql:
	docker exec -it kasparro-backend-hrishitha-bathula-db-1 psql -U postgres -d kasparro

test:
	pytest -v
