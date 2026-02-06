import argparse
import logging
from typing import TYPE_CHECKING

from api import WebServer
from api.health.handlers import HealthHandler
from config import settings
from fine_tuner import Factory

if TYPE_CHECKING:
    from fine_tuner import ResumeFineTuner

logger = logging.getLogger("main")


def init_args() -> argparse.Namespace:
    """Initialize command line arguments."""
    parser = argparse.ArgumentParser(description="Resume fine tuning application.")
    parser.add_argument("--serve", action="store_true", help="Run the web server.")
    return parser.parse_args()


def create_web_server(app: "ResumeFineTuner") -> WebServer:
    web = WebServer(resume_tuner=app)
    HealthHandler(server=web)
    return web

def main():
    app = Factory(cfg=settings)
    args = init_args()
    if args.serve:
        web = create_web_server(app=app)
        web.start()


if __name__ == "__main__":
    main()
