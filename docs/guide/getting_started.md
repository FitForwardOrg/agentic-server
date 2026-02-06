# Getting Started
Welcome to the Getting Started guide for setting up and running the backend project.
This guide will walk you through the necessary steps to get your development environment up and running.

## Prerequisites

1. Python 3.14 or higher
2. uv package manager (install via `pip install uv`)
   or `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Installation

1. Install packages 

```bash
make install
```

2. Generate docs

```bash
make docs
```

3. Open docs in a browser (optional)

```bash
make serve-doc # run in background http://0.0.0.0:8080/
```