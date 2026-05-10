"""
repositories/base.py — Generic Repository Interface
Student Assignment Tracker — Assignment 11

Defines the abstract base repository that all entity-specific repositories
must implement. Using Python generics (TypeVar) mirrors the Java
Repository<T, ID> pattern from the brief — one interface, zero duplication.

Design decisions:
- TypeVar T = the domain entity (Student, Assignment, etc.)
- TypeVar ID = the identifier type (str throughout this system)
- All methods raise NotImplementedError by default — concrete
  implementations must override every operation.
- exists() and count() are added beyond the brief's minimum four,
  because every real CRUD layer needs them and they prevent callers
  from doing find_by_id() just to check presence.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

# ---------------------------------------------------------------------------
# Generic type variables
# ---------------------------------------------------------------------------

T = TypeVar("T")   # Domain entity type
ID = TypeVar("ID") # Identifier type — str for all entities in this system


# ---------------------------------------------------------------------------
# Generic Repository Interface
# ---------------------------------------------------------------------------

class Repository(ABC, Generic[T, ID]):
    """
    Generic CRUD repository interface.

    All entity-specific repository interfaces extend this class and
    inherit the four standard operations. Additional query methods
    (e.g. find_by_status, find_by_course) are declared in the
    entity-specific interfaces below.
    """

    @abstractmethod
    def save(self, entity: T) -> None:
        """
        Persist an entity (insert or update).
        If an entity with the same ID already exists, it is overwritten.

        Args:
            entity: The domain object to persist.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """
        Retrieve a single entity by its unique identifier.

        Args:
            entity_id: The unique ID of the entity.

        Returns:
            The entity if found, None otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Retrieve all persisted entities of this type.

        Returns:
            A list of all entities (empty list if none exist).
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: ID) -> None:
        """
        Remove an entity by its unique identifier.

        Args:
            entity_id: The unique ID of the entity to remove.

        Raises:
            KeyError: If no entity with the given ID exists.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(self, entity_id: ID) -> bool:
        """
        Check whether an entity with the given ID exists.

        Args:
            entity_id: The unique ID to check.

        Returns:
            True if the entity exists, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """
        Return the total number of persisted entities.

        Returns:
            Integer count of stored entities.
        """
        raise NotImplementedError