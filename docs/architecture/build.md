# Build and Versioning

This document describes the build system and versioning scheme used for the Agentic Server.

## Build System

The project uses a `Makefile` to manage common tasks such as installing dependencies, running tests, building documentation, and building Docker images.

### Key Commands

- `make install`: Installs project dependencies using `uv`.
- `make test`: Runs unit tests with `pytest`.
- `make build`: Builds the Docker image.
- `make version-print`: Prints the current calculated version.

## Versioning Scheme

The application uses a dynamic versioning scheme based on the current date, git commit, and branch status.

### Version Format

The version string follows the format: `MMDDYYYY-HASH[-dev][-dirty]`

- **`MMDDYYYY`**: The current date in Month-Day-Year format (e.g., `02062026`).
- **`HASH`**: The first 7 characters of the current git command signature (SHA).
- **`-dev`**: Appended if the build is NOT from the `main` branch.
- **`-dirty`**: Appended if there are uncommitted changes in the repository at build time.

### Examples

| Scenario | Version Example |
| :------- | :-------------- |
| Release build from `main` | `02062026-c6c7c6d` |
| Development build from `feature/branch` | `02062026-c6c7c6d-dev` |
| Build with uncommitted changes | `02062026-c6c7c6d-dev-dirty` |

## Implementation Details

The versioning logic is implemented directly in the `Makefile` using standard shell and git commands:

```makefile
DATE := $(shell date +"%m%d%Y")
GIT_HASH := $(shell git rev-parse --short=7 HEAD)
GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
GIT_DIRTY := $(shell if [ -n "$$(git status --porcelain)" ]; then echo "-dirty"; fi)

ifeq ($(GIT_BRANCH),main)
    VERSION_SUFFIX := $(GIT_DIRTY)
else
    VERSION_SUFFIX := -dev$(GIT_DIRTY)
endif

VERSION ?= $(DATE)-$(GIT_HASH)$(VERSION_SUFFIX)
```
