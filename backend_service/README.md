# LLM Query Service

An LLM-powered query service built with FastAPI, LangChain, and PostgreSQL, featuring user authentication and daily query rate limiting...

## Features

- ✅ User registration and authentication with JWT
- ✅ LLM-powered query processing using LangChain and OpenAI
- ✅ Daily query rate limiting per user
- ✅ Query history tracking
- ✅ Query statistics and monitoring
- ✅ Redis-based rate limiting
- ✅ Comprehensive logging
- ✅ Full test coverage

## Project Structure

```
backend_llm_service/
├── src/
│   ├── api/                 # FastAPI routes and endpoints
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── query.py        # Query endpoints
│   │   ├── dependencies.py # Dependency injection
│   │   └── __init__.py
│   ├── core/               # Core business logic
│   │   ├── auth.py         # Password hashing and JWT
│   │   ├── rate_limiter.py # Rate limiting logic
│   │   ├── schemas.py      # Pydantic models
│   │   └── __init__.py
│   ├── services/           # Business logic services
│   │   ├── user_service.py # User CRUD operations
│   │   ├── llm_service.py  # LLM processing
│   │   └── __init__.py
│   ├── models/             # Database models
│   │   ├── user.py         # User model
│   │   ├── query_log.py    # Query log model
│   │   └── __init__.py
│   ├── db/                 # Database configuration
│   │   ├── database.py     # SQLAlchemy setup
│   │   └── __init__.py
│   ├── utils/              # Utility functions
│   │   ├── logger.py       # Logging configuration
│   │   └── __init__.py
│   └── main.py             # FastAPI application entry point
├── config/
│   └── settings.py         # Application settings
├── tests/                  # Unit and integration tests
│   ├── conftest.py         # Test configuration
│   ├── test_user_service.py
│   ├── test_rate_limiter.py
│   └── __init__.py
├── pyproject.toml          # Project configuration with UV
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- OpenAI API Key

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd backend_llm_service
```


### 3. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Install dependencies with UV

```bash
# create virtual env venv
uv venv

# Or using UV directly
uv sync
```

### 5. Set up the database

```bash
# Create database
psql -U postgres -c "CREATE DATABASE llm_db;"

# Run migrations (if using Alembic)
alembic upgrade head
```

### 6. Start Redis

```bash
# macOS/Linux
redis-server

# Windows (if installed via WSL or Docker)
redis-server
```

## Usage

### Start the server

```bash
# Using Uvicorn directly
uvicorn src.main:app --reload

# Or using Python
python -m src.main
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Register a new user

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

### Submit a query

```bash
curl -X POST "http://localhost:8000/api/v1/queries/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "What is the capital of France?"
  }'
```

### Check query statistics

```bash
curl -X GET "http://localhost:8000/api/v1/queries/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get query history

```bash
curl -X GET "http://localhost:8000/api/v1/queries/history?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Configuration

All configuration is managed through environment variables in `.env`:

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for LLM
- `LLM_MODEL`: Model to use (default: gpt-3.5-turbo)
- `SECRET_KEY`: JWT secret key
- `REDIS_URL`: Redis connection URL
- `MAX_QUERIES_PER_DAY`: Daily query limit per user (default: 10)
- `QUERY_RESET_HOUR`: Hour of day to reset queries (default: 0 UTC)

## Testing

Run tests with pytest:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src tests/

# Run specific test file
uv run pytest tests/test_user_service.py
```

## Development

### Install development dependencies

```bash
uv sync --extra dev
```

### Code formatting and linting

```bash
# Format code with Black
uv run black src tests

# Lint with Ruff
uv run ruff check src tests

# Type checking with mypy
uv run mypy src
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token

### Queries
- `POST /api/v1/queries/` - Submit a query
- `GET /api/v1/queries/history` - Get query history
- `GET /api/v1/queries/stats` - Get query statistics

### Health
- `GET /health` - Health check

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

## Rate Limiting

- Each user can make up to 10 queries per day (configurable)
- Rate limit resets at 00:00 UTC (configurable)
- Rate limiting is tracked in Redis
- When limit is exceeded, response includes reset time

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS protection enabled
- Environment-based configuration for secrets
- SQL injection protection through SQLAlchemy ORM

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
