"""
api/dependencies.py — FastAPI Dependency Injection
Student Assignment Tracker

Provides a single shared RepositoryFactory instance and service
factories that FastAPI injects into route handlers via Depends().

Using dependency injection here means:
- Tests can override get_factory() with a fresh in-memory factory
- The storage backend can be switched in one place
- Route handlers never import RepositoryFactory directly
"""

from __future__ import annotations

from functools import lru_cache
from repositories.factory import RepositoryFactory
from services.user_service import UserService
from services.assignment_service import AssignmentService
from services.submission_service import SubmissionService


@lru_cache(maxsize=1)
def get_factory() -> RepositoryFactory:
    """
    Return the application-wide RepositoryFactory.
    Cached — only one instance is created for the lifetime of the app.
    Override in tests via app.dependency_overrides[get_factory].
    """
    return RepositoryFactory("MEMORY")


def get_user_service(factory: RepositoryFactory = None) -> UserService:
    if factory is None:
        factory = get_factory()
    return UserService(factory)


def get_assignment_service(factory: RepositoryFactory = None) -> AssignmentService:
    if factory is None:
        factory = get_factory()
    return AssignmentService(factory)


def get_submission_service(factory: RepositoryFactory = None) -> SubmissionService:
    if factory is None:
        factory = get_factory()
    return SubmissionService(factory)