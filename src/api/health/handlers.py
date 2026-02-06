from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.api.health.models import StatusResponse

if TYPE_CHECKING:
    from src.api.server import WebServer


class HealthHandler:
    def __init__(self, server: WebServer):
        self.server = server
        self.router = APIRouter(prefix="/api/health", tags=["Health"])
        self._register_routes()

    def _register_routes(self):
        self.router.add_api_route(
            "/alive",
            self.is_alive,
            methods=["GET"],
            response_model=StatusResponse,
            summary="Liveness probe",
        )
        self.router.add_api_route(
            "/ready",
            self.is_ready,
            methods=["GET"],
            response_model=StatusResponse,
            summary="Readiness probe",
            responses={
                200: {
                    "description": "Service ready",
                    "content": {"application/json": {"example": StatusResponse(status="ready").model_dump()}},
                },
                503: {
                    "description": "Service not ready",
                    "content": {"application/json": {"example": StatusResponse(status="not ready").model_dump()}},
                },
            },
        )
        self.server.add_router(self.router)

    async def is_alive(self) -> StatusResponse:
        """Liveness probe."""
        return StatusResponse(status="alive")

    async def is_ready(self) -> StatusResponse:
        """Readiness probe."""
        if self.server.is_ready():
            return StatusResponse(status="ready")
        return JSONResponse(
            status_code=503,
            content=StatusResponse(status="not ready").model_dump(),
        )
