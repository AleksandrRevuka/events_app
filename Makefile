DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker-compose.yml
APP_CONTAINER = events_app

export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-migrate
app-migrate:
	${EXEC} ${APP_CONTAINER} bash -c "cd /app/event_api && poetry run python manage.py migrate"


.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make app              - Start the application with Docker Compose."
	@echo "  make app-down         - Stop the application."