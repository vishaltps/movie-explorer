# l7-informatics

Movie Explorer is a full-stack interview project with a FastAPI backend and a React + Vite frontend. The backend serves a read-only movie catalog with filtering and detail endpoints; the frontend consumes that API, keeps filters in the URL, and stores favorites locally.

## Stack

- Backend: FastAPI, SQLAlchemy, Alembic, SQLite, pytest
- Frontend: React 18, TypeScript, Vite, React Router, TanStack Query, Tailwind CSS, Vitest, MSW
- Tooling: `uv`, npm, Docker Compose, GitHub Actions

## Backend

### Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

### Setup

```bash
cd backend
uv sync
```

### Run API

```bash
make dev
```

The API runs on `http://localhost:8000`, Swagger UI is at `http://localhost:8000/docs`, and OpenAPI JSON is at `http://localhost:8000/api/v1/openapi.json`.

### Migrate + seed

```bash
make migrate
make seed
```

### Test + lint

```bash
make lint
make test
```

## Frontend

### Requirements

- Node.js 20+
- npm 10+

### Setup

```bash
cd frontend
npm install
```

### Run app

```bash
npm run dev
```

The frontend dev server runs on `http://localhost:5173` by default. By default the app uses `/api/v1`, and the Vite dev server proxies that to `http://127.0.0.1:8000`, so you usually do not need to set `VITE_API_BASE_URL` for local development.

### Frontend checks

```bash
npm run lint
npm run test
npm run build
```

### Regenerate API types

The backend must be running locally before regenerating the frontend types.

```bash
cd backend
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In a second terminal:

```bash
cd frontend
npm run gen:types
```

This updates [`frontend/src/shared/types/api-generated.ts`](./frontend/src/shared/types/api-generated.ts).

## Full stack with Docker

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

The compose setup runs migrations and seeds the SQLite database automatically before starting the API. The nginx frontend proxies `/api/v1/*` to the backend service, so the browser does not need to resolve the internal Docker hostname.
