import json
from pathlib import Path

import click
from fastapi.openapi.utils import get_openapi

from src.main import create_web_server


def discover_tags() -> list[str]:
    """Discover all unique tags used in the application routes."""
    web = create_web_server(app=None)
    app = web.app
    tags = set()
    for route in app.routes:
        if hasattr(route, "tags"):
            for tag in route.tags:
                tags.add(tag)
    return sorted(list(tags))


def generate_schema(tags: list[str] | None = None, suffix: str | None = None):
    print("Generating OpenAPI schema...")

    web = create_web_server(app=None)
    app = web.app

    routes = app.routes
    if tags:
        routes = [r for r in app.routes if hasattr(r, "tags") and any(tag in r.tags for tag in tags)]

    schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=routes,
        servers=[
            {"url": "http://localhost:8000", "description": "Local developer server"},
        ],
    )

    filename = f"openapi_{suffix}.json" if suffix else "openapi.json"
    output_path = Path("docs/specs") / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2)

    print(f"Schema generated at {output_path}")


@click.command()
@click.option(
    "--tags",
    multiple=True,
    type=click.Choice(discover_tags(), case_sensitive=False),
    help="List of tags to filter routes by.",
)
@click.option("--suffix", help="Suffix for the output filename (openapi_{suffix}.json).")
def main(tags, suffix):
    """Generate OpenAPI schema."""
    generate_schema(tags=list(tags) if tags else None, suffix=suffix)


if __name__ == "__main__":
    main()
