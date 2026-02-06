.DEFAULT_GOAL := help

# Get version information
DATE := $(shell date +"%m%d%Y")
GIT_HASH := $(shell git rev-parse --short=7 HEAD 2>/dev/null || (echo "$$GITHUB_SHA" | cut -c1-7))
GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
GIT_DIRTY := $(shell if [ -n "$$(git status --porcelain)" ]; then echo "-dirty"; fi)

# Determine the version suffix based on the branch and dirty status
ifeq ($(GIT_BRANCH),main)
    VERSION_SUFFIX := $(GIT_DIRTY)
else
    VERSION_SUFFIX := -dev$(GIT_DIRTY)
endif

VERSION ?= $(DATE)-$(GIT_HASH)$(VERSION_SUFFIX)
IMAGE ?= agentic-server
TAG ?= latest

SKIP_TESTS ?= false


.PHONY: version-print
version-print: ## Prints the current version
	@echo $(VERSION)

.PHONY: install
install: ## Installs dependencies
	uv sync

.PHONY: doc
doc: schema ## Builds documentation
	PYTHONPATH=.:src uv run mkdocs build
	@echo "Documentation built in site/"

.PHONY: schema
schema: ## Generates OpenAPI schema
	PYTHONPATH=.:src uv run python src/scripts/generate_schema.py --tags Health --suffix health

.PHONY: serve-doc
serve-doc: ## Serves documentation
	PYTHONPATH=.:src uv run mkdocs serve --dev-addr 0.0.0.0:8080

.PHONY: format
format: ## Formats code
	uv run ruff check --fix .
	uv run ruff format .

.PHONY: lint
lint: ## Runs linter
	uv run ruff check .

.PHONY: hooks
hooks: ## Installs git hooks (runs make lint on commit)
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit

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
	PYTHONPATH=. uv run ./src/main.py serve

.PHONY: build
build: ## Builds the Docker image
	docker build \
		--build-arg COMMIT=$(GIT_HASH) \
		--build-arg VERSION=$(VERSION) \
		--build-arg SKIP_TESTS=$(SKIP_TESTS) \
		-t $(IMAGE):$(TAG) .

.PHONY: run-docker
run-docker: ## Runs the application in Docker
	docker run -it -p 8000:8000 $(IMAGE):$(TAG)

.PHONY: help
help: ## Displays brief description of each build target
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
