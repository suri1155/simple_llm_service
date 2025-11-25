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
1. OPENAI_API_KEY
    - Get your OPENAI_API_KEY from [https://platform.openai.com](https://platform.openai.com)
    - supported models: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, etc.


**Notes & Links**
- set .env file for backend_service, refer [backend_service\README.md](backend_service\README.md)
- To spin up the entire stack quickly, read `docker_running.md` at the repository root.

**Start End to End Application**
```bash
docker-compose up --build
```

See `docker_running.md` for more details on running and troubleshooting the containers.


## License

MIT License

## Support

For issues and questions, please create an issue in the repository.