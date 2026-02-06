.DEFAULT_GOAL := help

# Get version information
GIT_COMMIT := $(shell git rev-parse --short=10 HEAD)
DESCRIBE := $(subst -, ,$(subst release/,,$(shell git describe --match 'release/*' --abbrev=10 --dirty=+m)))

# Go through a nasty dance to determine whether we are on a dev/rc tag, which shifts the output
# of `git describe` right by one because our tags can look like `release/1.2.3-dev1`.
#
# The field separator for `git describe` is '-' so dev/rc tags are harder to parse out.
SUFFIX =
ifeq ($(or $(findstring dev,$(word 2, $(DESCRIBE))),$(findstring rc,$(word 2, $(DESCRIBE)))),)
# A standard release tag -- `git describe` does not contain dev or rc
DELTA = 0
ifneq ($(words $(DESCRIBE)),1)
# We are 1+ commits past the tag
DELTA = $(word 2, $(DESCRIBE))
endif
else
# A dev/rc release tag
SUFFIX = -$(word 2, $(DESCRIBE))
DELTA = 0
ifneq ($(words $(DESCRIBE)),2)
# We are 1+ commits past the tag
DELTA = $(word 3, $(DESCRIBE))
endif
endif

# Are there local, uncommitted changes at build time?
DIRTY := $(subst +,-,$(findstring +m,$(lastword $(DESCRIBE))))

# Set the RT (release train) component; will include dev or rc as appropriate
RT := $(word 1, $(DESCRIBE))$(SUFFIX)

ifeq ($(DELTA), 0)
VERSION ?= $(RT)
else
VERSION ?= $(RT)-$(DELTA)-$(GIT_COMMIT)$(DIRTY)
endif

SKIP_TESTS ?= false


.PHONY: install
install: ## Installs dependencies
	uv sync

.PHONY: doc
doc: schema ## Builds documentation
	uv run mkdocs build
	@echo "Documentation built in site/"

.PHONY: schema
schema: ## Generates OpenAPI schema
	PYTHONPATH=.:src uv run python src/scripts/generate_schema.py --tags Health --suffix health

.PHONY: serve-doc
serve-doc: ## Serves documentation
	uv run mkdocs serve --dev-addr 0.0.0.0:8080

.PHONY: format
format: ## Formats code
	uv run ruff check --fix .
	uv run ruff format .

.PHONY: lint
lint: ## Runs linter
	uv run ruff check .

.PHONY: test
test: ## Runs tests
	PYTHONPATH=.:src uv run pytest

.PHONY: clean
clean: ## Cleans up generated files
	rm -rf ./site/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: run
run: ## Runs the application locally with auto-reload
	PYTHONPATH=. uv run ./src/main.py --serve

.PHONY: build
build: ## Builds the Docker image
	docker build \
		--build-arg COMMIT=$(GIT_COMMIT) \
		--build-arg VERSION=$(VERSION) \
		--build-arg SKIP_TESTS=$(SKIP_TESTS) \
		-t agentic-server .

.PHONY: run-docker
run-docker: ## Runs the application in Docker
	docker run -it -p 8000:8000 agentic-server

.PHONY: help
help: ## Displays brief description of each build target
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
