# LLM Query Service

An LLM-powered query service built with FastAPI, LangChain, and PostgreSQL, featuring user authentication and daily query rate limiting...

## Features

-  User registration and authentication with JWT
-  LLM-powered query processing using LangChain and OpenAI
-  Daily query rate limiting per user
-  Query history tracking
-  Query statistics and monitoring
-  Redis-based rate limiting
-  Comprehensive logging
-  Full test coverage

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
├── pyproject.toml          # Project configuration with UV
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Prerequisites

- Python 3.12+
- OpenAI API Key

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd backend_service
```

### 3. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```



### Code formatting and linting

```bash
# Format code with Black
uv run black src

# Lint with Ruff
uv run ruff check src --fix

# Type checking with mypy
uv run mypy src
```

