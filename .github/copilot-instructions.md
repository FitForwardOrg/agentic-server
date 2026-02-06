# Copilot instructions (agentic-server)

## Tech + style
- Python 3.14, FastAPI, `uv` tooling, `pytest` tests, `ruff` for lint/format (`line-length = 120`, double quotes).
- Prefer type hints everywhere; keep functions small and focused; use clear docstrings on public APIs/tools.
- Keep I/O (web/db/LLM) at the edges; keep core logic pure and testable.

## Project conventions
- Put server/API code under `src/`; tests under `tests/`.
- Don’t edit generated artifacts (e.g., `src/__pycache__/`, `src/*.egg-info/`).
- Follow existing patterns in nearby files; avoid large refactors unless asked.

## Common commands
- Lint/format: `uv run ruff check --fix . && uv run ruff format .`
- Tests: `PYTHONPATH=.:src uv run pytest`
