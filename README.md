# simple_llm_service

This repository contains a small end-to-end example LLM application. The project demonstrates a minimal production-like setup with a FastAPI backend serving a LangChain-based LLM service, a React frontend, PostgreSQL for persistent storage, and Redis for caching/rate-limiting.

**Overview**
- **Purpose**: Example app showing how to wire a simple LLM service into a web app with persistent storage and caching.
- **Backend**: `backend_service` — FastAPI app exposing API endpoints and the LangChain-powered LLM service.
- **Frontend**: `frontend_service` — React app that interacts with the backend.
- **Data stores**: PostgreSQL for storing application data (users, query logs) and Redis for caching and rate limiting.

**Tech Stack**
- **LLM / Orchestration**: LangChain
- **API**: FastAPI + Uvicorn
- **Frontend**: React
- **DB / Cache**: PostgreSQL, Redis
- **Containerization**: Docker & Docker Compose

**Repository Layout**
- `backend_service/` — backend implementation, configs, and its own `README.md`.
- `frontend_service/` — React frontend and its `README.md`.
- `docker-compose.yml` — orchestrates backend, frontend, Postgres, Redis, and other services.
- `docker_running.md` — notes and commands for spinning up the full stack with Docker Compose.



**OpenAI Model Configuration**

This application uses OpenAI models via LangChain. To use the service, you need:

1. **Obtain an OpenAI API Key**
   - Sign up at [https://platform.openai.com](https://platform.openai.com)
   - Generate an API key from your account settings
   - Keep this key secure (never commit it to version control)

2. **Set Environment Variables**
   - `OPENAI_API_KEY`: Your OpenAI API key (required)
   - `LLM_MODEL`: The model to use (default: `gpt-3.5-turbo`)
     - Supported models: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, etc.
     - Check [OpenAI documentation](https://platform.openai.com/docs/models) for latest available models

3. **Local Setup**
   - Create a `.env` file in `backend_service/` directory:
    Note:refer .env.example for template
     ```
     OPENAI_API_KEY=sk-your-api-key-here
     LLM_MODEL=gpt-3.5-turbo
     ```

**Quickstart (Docker)**
1. Build images (if you haven't already):

```powershell
docker-compose build
```

2. Start the full stack:

```powershell
docker-compose up -d
```

3. To view logs for a service (example: backend):

```powershell
docker-compose logs -f backend_service
```

See `docker_running.md` for more details on running and troubleshooting the containers.

**Run Locally (Backend)**
- See `backend_service/README.md` for environment variables, local virtual environment setup, and commands to run the FastAPI server directly (without Docker).

**Run Locally (Frontend)**
- See `frontend_service/README.md` for instructions to install dependencies and run the React development server.

**Tests**
- Backend tests are located in `backend_service/tests/`. Run them from the `backend_service` directory using:

```powershell
cd backend_service
pytest -q
```

**Notes & Links**
- For backend configuration and settings, check `backend_service/config/settings.py`.
- For database migrations or schema changes, follow the docs in `backend_service/README.md`.
- To spin up the entire stack quickly, read `docker_running.md` at the repository root.


