"""
repositories/inmemory/base_inmemory.py — Base In-Memory Repository
Student Assignment Tracker — Assignment 11

Provides the shared HashMap (dict) storage logic used by all in-memory
implementations. Concrete repositories inherit this and only need to
implement their entity-specific finder methods.

Design decisions:
- _storage is a plain Python dict — equivalent to Java's HashMap<ID, T>
- All six generic CRUD methods are implemented here once — no duplication
  across the nine entity repositories
- delete() raises KeyError if the ID doesn't exist — fail loudly rather
  than silently ignoring a missing delete (easier to catch bugs)
- find_all() returns a copy of values — callers cannot mutate internal state
"""

from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

from repositories.base import Repository

T = TypeVar("T")
ID = TypeVar("ID")


class InMemoryRepository(Repository[T, ID], Generic[T, ID]):
    """
    Generic in-memory repository backed by a Python dict (HashMap).
    All nine entity repositories extend this class and inherit
    full CRUD behaviour for free.
    """

    def __init__(self):
        self._storage: dict = {}  # { entity_id: entity }

    # ------------------------------------------------------------------ #
    # Generic CRUD — implemented once, inherited by all subclasses
    # ------------------------------------------------------------------ #

    def save(self, entity: T) -> None:
        """Insert or overwrite an entity keyed by its ID."""
        entity_id = self._get_id(entity)
        self._storage[entity_id] = entity

    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Return entity by ID, or None if not found."""
        return self._storage.get(entity_id)

    def find_all(self) -> List[T]:
        """Return a snapshot list of all stored entities."""
        return list(self._storage.values())

    def delete(self, entity_id: ID) -> None:
        """
        Remove entity by ID.
        Raises KeyError if the ID does not exist — fail loudly.
        """
        if entity_id not in self._storage:
            raise KeyError(f"No entity with id '{entity_id}' found.")
        del self._storage[entity_id]

    def exists(self, entity_id: ID) -> bool:
        """Return True if an entity with this ID is stored."""
        return entity_id in self._storage

    def count(self) -> int:
        """Return total number of stored entities."""
        return len(self._storage)

    # ------------------------------------------------------------------ #
    # Internal helper — subclasses override if ID lives on a different attr
    # ------------------------------------------------------------------ #

    def _get_id(self, entity: T) -> ID:
        """
        Extract the ID from an entity.
        Tries common ID attribute names in order.
        Override in subclasses if the entity uses a non-standard field.
        """
        for attr in ("user_id", "student_id", "lecturer_id", "course_id",
                     "assignment_id", "submission_id", "grade_id",
                     "notification_id", "enrollment_id"):
            if hasattr(entity, attr):
                return getattr(entity, attr)
        raise AttributeError(
            f"Cannot determine ID for entity of type {type(entity).__name__}. "
            f"Override _get_id() in the concrete repository."
        )