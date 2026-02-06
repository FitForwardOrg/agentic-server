# Configuration

The Agentic Server can be configured using environment variables. This guide outlines the available settings and how to manage them.

## Environment Variables

We use `.env` files for local development. A template is provided in `.env.example`.

### Application Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | The name of the application | `Agentic Server` |
| `APP_VERSION` | The version of the application | `0.1.0` |
| `DEBUG` | Enable debug mode (True/False) | `False` |

### API Server Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | The host address to bind the server to | `0.0.0.0` |
| `PORT` | The port to run the server on | `8000` |

## Local Development

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Adjust the values in `.env` as needed.
3. The application will automatically load these settings when run.
