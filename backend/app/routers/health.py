"""Health check endpoint — Docker readiness probe."""

from fastapi import APIRouter, Request

from app.data_services.base import ok
from app.schemas.envelope import Envelope

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health", response_model=Envelope[dict[str, str]], summary="Readiness check")
def health(request: Request) -> Envelope[dict[str, str]]:
    return ok({"status": "ok"}, request_id=getattr(request.state, "request_id", None))
