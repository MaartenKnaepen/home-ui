# Agents & Coding Standards

## Python Standards
- **Version:** Python 3.10+
- **Typing:** Use modern type hints (`str | None` instead of `Optional[str]`, `list[str]` instead of `List[str]`).
- **Style:** PEP 8 compliance.
- **Frameworks:** FastAPI for web, Pydantic for data validation.
- **Error Handling:** Fail gracefully, log errors, return appropriate HTTP status codes.

## Security
- **Secrets:** NEVER hardcode passwords or keys. Use `os.getenv` or `pydantic-settings`.
- **Auth:** Use HttpOnly, Secure cookies for session management.

## Docker
- **Images:** Use slim variants (e.g., `python:3.11-slim`).
- **User:** Run containers as non-root user where possible.

## Frontend
- **Tech:** Jinja2 templates + TailwindCSS (CDN).
- **Structure:** Keep logic in Python, presentation in HTML.
