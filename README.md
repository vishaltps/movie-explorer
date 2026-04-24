# Movie Explorer

A full-stack movie catalog built with FastAPI and React. Browse and filter movies, actors, directors, and genres. Favorites are saved to local storage.

## Stack

- **Backend:** FastAPI, SQLAlchemy, Alembic, SQLite, pytest
- **Frontend:** React 18, TypeScript, Vite, React Router, TanStack Query, Tailwind CSS, Vitest, MSW
- **Tooling:** `uv`, npm, Docker Compose, GitHub Actions

## Requirements

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose (for the one-command setup)
- Python 3.12+ and [uv](https://github.com/astral-sh/uv) (for local backend development)
- Node.js 20+ and npm 10+ (for local frontend development)

## Quick start with Docker

The fastest way to run the full stack — no local Python or Node setup required:

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:8080 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| OpenAPI JSON | http://localhost:8000/api/v1/openapi.json |

Migrations and seed data run automatically on first boot. The nginx frontend proxies `/api/v1/*` to the backend container, so no CORS configuration is needed.

## Backend (local development)

```bash
cd backend
uv sync          # install dependencies
make migrate     # run Alembic migrations
make seed        # load curated seed data (40 movies, 17 genres, 53 actors)
make dev         # start API on http://localhost:8000
```

### Test + lint

```bash
make lint        # ruff check + format + mypy
make test        # pytest with 85% coverage gate
```

## Frontend (local development)

Start the backend first (see above), then in a separate terminal:

```bash
cd frontend
npm install      # install dependencies
npm run dev      # start dev server on http://localhost:5173
```

The Vite dev server proxies `/api/v1/*` to `http://127.0.0.1:8000` automatically.

### Checks

```bash
npm run lint     # eslint
npm run test     # vitest with coverage
npm run build    # tsc + vite build
```

### Regenerate API types

The backend must be running before regenerating types from the OpenAPI spec:

```bash
# Terminal 1 — backend
cd backend && make dev

# Terminal 2 — regenerate
cd frontend && npm run gen:types
```

This updates [`frontend/src/shared/types/api-generated.ts`](./frontend/src/shared/types/api-generated.ts). The CI workflow checks that committed types match the live spec on every push.
