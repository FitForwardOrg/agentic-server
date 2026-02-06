# Agentic Server Documentation

AI-powered resume tailoring service built with Python 3.14 + FastAPI. Parses user resumes and job descriptions, generates contextual Q&A to bridge skill gaps, and uses AI to rewrite resumes with ATS-optimized keywords and personalized cover letters. Modular architecture on PostgreSQL, designed for MVP deployment.

**Key Features**:

* Resume & JD parsing with semantic analysis
* Intelligent gap-detection Q&A generation
* AI-driven resume rewriting with match scoring
* DOCX/PDF export with formatting preservation
* JWT authentication & session management

**Stack**: Python 3.14 + FastAPI | uv + ruff | PostgreSQL | OpenAI API | Docker | Datadog observability

## Sections

- [Guide](guide/index.md): User guides and tutorials.
- [Architecture](architecture/index.md): System architecture and design.
- [API Reference](api/index.md): API documentation.
