# backend — notes API (FastAPI + PostgreSQL)

Dependencies are managed with **uv** (`pyproject.toml` + `uv.lock`).

```bash
# local Postgres
docker run -d --name pg-local -p 5433:5432 \
  -e POSTGRES_USER=dev -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=dev postgres:16

cd backend
uv sync                                    # creates .venv with app + dev deps
export DATABASE_URL=postgresql+psycopg://dev:dev@localhost:5433/dev
uv run pytest -q                           # 3 passed
uv run uvicorn app.main:app --reload       # http://localhost:8000/api/docs

# container, exactly as production runs it
docker build -t fastapi-demo-api:local --build-arg APP_VERSION=local .
docker run --rm -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg://dev:dev@host.docker.internal:5433/dev \
  fastapi-demo-api:local
curl -s localhost:8000/api/health          # {"status":"ok","version":"local"}
```

Add a package: `uv add <pkg>` (runtime) or `uv add --dev <pkg>` (tests only). Commit `uv.lock`.
