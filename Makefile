.PHONY: app
app:
	docker compose up -d --build

.PHONY: app-down
app-down:
	docker compose down
	
.PHONY: prod
prod:
	docker compose -f docker-compose.production.yml up -d --build

.PHONY: prod-down
prod-down:
	docker-compose -f docker-compose.production.yml down

.PHONY: logs
logs:
	docker compose logs

.PHONY: tests
tests:
	poetry run 
