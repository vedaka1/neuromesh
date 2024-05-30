.PHONY: app
app:
	docker compose up -d --build

.PHONY: app-down
app-down:
	docker compose down

.PHONY: logs
logs:
	docker compose logs

.PHONY: tests
tests:
	poetry run 
