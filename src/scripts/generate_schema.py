import argparse
import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from src.main import create_web_server


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
        ]
    )

    # Output path assumed to be relative to project root when run via Makefile
    filename = f"openapi_{suffix}.json" if suffix else "openapi.json"
    output_path = Path("docs/specs") / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(schema, f, indent=2)

    print(f"Schema generated at {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate OpenAPI schema")
    parser.add_argument("--tags", nargs="*", help="List of tags to filter routes by")
    parser.add_argument("--suffix", help="Suffix for the output filename (openapi_{suffix}.json)")

    args = parser.parse_args()
    generate_schema(tags=args.tags, suffix=args.suffix)
