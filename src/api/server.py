import logging
from typing import TYPE_CHECKING

import uvicorn
from fastapi import FastAPI, APIRouter

from config import settings

if TYPE_CHECKING:
    from src.fine_tuner import ResumeFineTuner

logger = logging.getLogger(__name__)

class WebServer:
    """
    Represents a web server for the backend application.
    """

    def __init__(self, resume_tuner: "ResumeFineTuner"):
        self.resume_tuner = resume_tuner
        self.app: FastAPI = FastAPI(
            title=settings.app_name,
            version=settings.app_version,
            docs_url=None,  # Disable Swagger UI
            redoc_url=None,  # Disable Redoc
            openapi_url="/openapi.json",
        )

    def add_router(self, router: APIRouter):
        """ Add a router to the application."""
        self.app.include_router(router)

    def is_ready(self) -> bool:
        """Check if the server and its components are ready."""
        return self.resume_tuner.is_ready()

    def start(self):
        """Start the web server."""
        logger.info(f"Starting web server {settings.app_version}...")
        uvicorn.run(self.app, host=settings.host, port=settings.port, reload=settings.debug)
