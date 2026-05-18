"""
services/base.py — Base Service
Student Assignment Tracker

Provides shared validation helpers and a common exception hierarchy
used across all service classes.

Exception hierarchy:
    ServiceError                  ← base for all service errors
        ├── NotFoundError         ← entity doesn't exist (→ HTTP 404)
        ├── ValidationError       ← invalid input data (→ HTTP 422)
        ├── ConflictError         ← business rule violation (→ HTTP 409)
        └── PermissionError       ← unauthorised action (→ HTTP 403)
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------

class ServiceError(Exception):
    """Base class for all service-layer exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(ServiceError):
    """Raised when a requested entity does not exist."""
    def __init__(self, entity: str, entity_id: str):
        super().__init__(f"{entity} with id '{entity_id}' not found.")
        self.entity = entity
        self.entity_id = entity_id


class ValidationError(ServiceError):
    """Raised when input data fails validation rules."""
    pass


class ConflictError(ServiceError):
    """Raised when a business rule would be violated."""
    pass


class PermissionError(ServiceError):
    """Raised when an actor attempts an unauthorised action."""
    pass


# ---------------------------------------------------------------------------
# Shared validation helpers
# ---------------------------------------------------------------------------

class BaseService:
    """
    Base class for all service classes.
    Provides common validation utilities inherited by every service.
    """

    @staticmethod
    def _require(value: str, field_name: str) -> str:
        """Assert a string field is non-empty after stripping whitespace."""
        if not value or not str(value).strip():
            raise ValidationError(f"'{field_name}' is required and cannot be empty.")
        return str(value).strip()

    @staticmethod
    def _require_positive(value: int | float, field_name: str) -> int | float:
        """Assert a numeric value is greater than zero."""
        if value is None or value <= 0:
            raise ValidationError(f"'{field_name}' must be greater than zero.")
        return value

    @staticmethod
    def _require_not_none(value, field_name: str):
        """Assert a value is not None."""
        if value is None:
            raise ValidationError(f"'{field_name}' is required.")
        return value