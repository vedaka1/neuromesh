DC = docker compose
DEV = docker-compose.yml
PROD = docker-compose.production.yml

dev:
	$(DC) -f $(DEV) up -d --build
	
prod:
	$(DC) -f $(PROD) up -d --build

logs:
	$(DC) -f $(DEV) -f $(PROD)  logs

down:
	$(DC) -f $(DEV) -f $(PROD) down

PHONY: tests
