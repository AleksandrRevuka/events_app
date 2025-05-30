# Event Management API (Django)

## 📝 Overview
The **Event Management API** is a Django-based backend for managing events and user registrations. It supports full CRUD operations for both events and registrations and is designed for scalable deployment using Docker.

## Requirements
To run the API, ensure you have the following installed:

- Docker and Docker Compose
- Python 3.12+

## Environment Variables

Create a `.env` file in the root of your project with the following content:

```env
# Database Configuration
DATABASE_HOST=your_database_host
DATABASE_PORT=5432
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_NAME=your_database_name

SECRET_KEY=your-super-secret-key
DEBUG=True
```

## Commands
You can interact with the application using the following commands, either directly or via the Makefile.

#### Start the Application:
```bash
docker compose -f docker-compose.yml --env-file .env up --build -d
```

#### Stop the Application:
```bash
docker compose -f docker-compose.yml down
```

#### View Application Logs:
```bash
docker logs events_app -f
```

#### Access Application Shell:
```bash
docker exec -it events_app bash
```

#### Make Migrations:
```bash
docker exec -it events_app bash -c "cd /app/event_api && poetry run python manage.py makemigrations"
```

#### Run Migrations:
```bash
docker exec -it events_app bash -c "cd /app/event_api && poetry run python manage.py migrate"
```

## Makefile Commands
The following commands can be run using the Makefile:

### Start the Application:
```bash
make app
```

### Stop the Application:
```bash
make app-down
```

### View Application Logs:
```bash
make app-logs
```

### Access Application Shell:
```bash
make app-shell
```

### Make Migrations:
```bash
make app-makemigrations
```

### Run Migrations:
```bash
make app-migrate
```

### Help:
```bash
make help
```

## Additional Notes
- Ensure that all necessary environment variables are correctly set before starting the application.
- Use the Makefile commands to simplify working with the application and its services.
- The `SECRET_KEY` is used for securing authentication and must remain confidential. 
