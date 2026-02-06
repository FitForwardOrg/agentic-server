import logging
from typing import TYPE_CHECKING

import click

from src.api import WebServer
from src.api.health.handlers import HealthHandler
from src.config import settings
from src.fine_tuner import factory

if TYPE_CHECKING:
    from fine_tuner import ResumeFineTuner

logger = logging.getLogger("main")


def create_web_server(app: "ResumeFineTuner") -> WebServer:
    web = WebServer(resume_tuner=app)
    HealthHandler(server=web)
    return web


@click.group()
def main():
    """Main entrypoint."""
    pass


@main.command()
def serve():
    """Run the web server."""
    app = factory(cfg=settings)
    web = create_web_server(app=app)
    web.start()


if __name__ == "__main__":
    main()
