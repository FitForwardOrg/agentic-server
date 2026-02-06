---
applyTo: '**/*.py'
---
# Python code style instructions

Target Python style: **Python 3.14+**, typed, clean, testable, and production-ready.

## Code style guidelines

When generating Python code:

* Use **FastAPI best practices**

  * Dependency injection via `Depends`
  * Pydantic models for request/response
  * Clear separation between API and business logic
* Prefer **small, composable functions**
* Add **type hints** everywhere
* Write **docstrings** for public classes and functions
* Avoid global state
* Follow **ruff-compatible formatting**

  * Double quotes
  * 120 char line limit
* Raise explicit exceptions, don’t silently fail
* Keep API handlers thin; business logic belongs in `fine_tuner`

## Architecture expectations

Copilot should:

* Respect existing folder structure
* Avoid circular dependencies
* Keep API layer independent from infrastructure
* Prefer dependency injection over direct imports
* Write code that is easy to mock and test
* Use testing guidelines from `.github/instructions/pytest.instructions.md`
* ensure all new code is covered by tests