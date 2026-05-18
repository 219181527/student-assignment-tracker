"""
api/main.py — FastAPI Application Entry Point
Student Assignment Tracker

Starts the FastAPI application, registers all routers, configures
OpenAPI metadata, and sets up global exception handlers.

Run locally:
    uvicorn api.main:app --reload

Swagger UI:    http://localhost:8000/docs
ReDoc:         http://localhost:8000/redoc
OpenAPI JSON:  http://localhost:8000/openapi.json
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routes import users, assignments, submissions
from services.base import (
    ServiceError, NotFoundError, ValidationError,
    ConflictError, PermissionError,
)

# ---------------------------------------------------------------------------
# Application instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Student Assignment Tracker API",
    description="""
A RESTful API for managing academic assignments, submissions, and grading.

## Features
- **User Management** — Register students and lecturers, authenticate, update profiles
- **Assignment Lifecycle** — Create, publish, close, and delete assignments
- **Submission & Grading** — Submit work, enforce enrollment rules, grade submissions

## Architecture
```
Client → API Layer → Service Layer → Repository Layer → Storage
```

## Authentication
This API uses role-based access. Pass `lecturer_id` or `student_id` in
request bodies to identify the acting user. Full JWT authentication is
planned for a future release.
    """,
    version="1.0.0",
    contact={
        "name": "Mongameli Shasha",
        "url": "https://github.com/219181527/student-assignment-tracker",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "Users",
            "description": "Student and lecturer registration, login, and profile management.",
        },
        {
            "name": "Assignments",
            "description": "Create, update, publish, close, and delete assignments.",
        },
        {
            "name": "Submissions",
            "description": "Submit assignments and manage grading.",
        },
    ],
)

# ---------------------------------------------------------------------------
# Global exception handlers — map service errors to HTTP responses
# ---------------------------------------------------------------------------

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "NotFoundError", "detail": exc.message},
    )


@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "ValidationError", "detail": exc.message},
    )


@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content={"error": "ConflictError", "detail": exc.message},
    )


@app.exception_handler(PermissionError)
async def permission_handler(request: Request, exc: PermissionError):
    return JSONResponse(
        status_code=403,
        content={"error": "PermissionError", "detail": exc.message},
    )


@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError):
    return JSONResponse(
        status_code=500,
        content={"error": "ServiceError", "detail": exc.message},
    )

# ---------------------------------------------------------------------------
# Register routers
# ---------------------------------------------------------------------------

app.include_router(users.router)
app.include_router(assignments.router)
app.include_router(submissions.router)


# ---------------------------------------------------------------------------
# Custom ReDoc (fixes blank page caused by CDN issues)
# ---------------------------------------------------------------------------

from fastapi.responses import HTMLResponse

@app.get("/redoc", include_in_schema=False)
def redoc():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
  <head>
    <title>Student Assignment Tracker API - ReDoc</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>body { margin: 0; padding: 0; }</style>
  </head>
  <body>
    <redoc spec-url='/openapi.json'></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
  </body>
</html>
    """)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Health"], summary="Health check")
def health():
    """Returns 200 OK if the API is running."""
    return {"status": "ok", "service": "Student Assignment Tracker API"}