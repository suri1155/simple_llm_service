### Start everything

```bash
docker-compose up --build
```

### Run backend only (Postgres + Redis will auto-start if needed)

```bash
docker-compose up -d backend
```

### Run frontend only

```bash
docker-compose up frontend
```

### Stop everything

```bash
docker-compose down
```

# Other helpful Docker commands
```bash
# View Logs
docker-compose logs -f

# Restart Service
docker-compose restart frontend

# Rebuild Single Service
docker-compose build frontend && docker-compose up -d frontend
# Rebuild Single Service without cache
docker-compose build --no-cache frontend && docker-compose up -d frontend

# Clean Everything
docker-compose down -v
docker system prune -a

# Check Status
docker-compose ps

# View Networks
docker network ls
```
