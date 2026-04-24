from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import get_settings
from app.exception_handlers import (
    app_error_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_error_handler,
)
from app.exceptions import AppError
from app.logging_config import configure_logging
from app.middleware import RequestIDMiddleware
from app.routers import actors, directors, genres, health, movies, reviews


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    del app
    configure_logging()
    yield


settings = get_settings()

app = FastAPI(
    title="Movie Explorer API",
    version="0.1.0",
    description=(
        "REST API for browsing movies, actors, directors, and genres.\n\n"
        "All responses use a consistent envelope: "
        "`{ success, data, error, meta }`. "
        "Errors include a stable `code`, human-readable `message`, "
        "and a `request_id` in `meta` for log correlation."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
    openapi_tags=[
        {"name": "Movies", "description": "Browse, filter, and view movie details."},
        {"name": "Actors", "description": "Browse actors and their filmographies."},
        {"name": "Directors", "description": "Browse directors and their filmographies."},
        {"name": "Genres", "description": "Browse genres."},
        {"name": "Reviews", "description": "Movie reviews."},
        {"name": "Health", "description": "Service readiness check."},
    ],
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(health.router)
app.include_router(genres.router)
app.include_router(directors.router)
app.include_router(actors.router)
app.include_router(movies.router)
app.include_router(reviews.router)
