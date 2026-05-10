"""
repositories/filesystem/base_filesystem.py — Base FileSystem Repository
Student Assignment Tracker — Assignment 11, Task 4

Provides shared JSON file read/write logic for all filesystem
repository implementations.

How it works:
- Each entity type gets its own JSON file (e.g. data/students.json)
- The file stores a flat dict: { "entity_id": { ...serialized fields... } }
- On every save/delete the entire file is rewritten (suitable for small
  datasets; a real production system would use a database instead)
- Subclasses override _serialize() and _deserialize() to convert between
  domain objects and plain dicts

This is a STUB implementation — _serialize() and _deserialize() raise
NotImplementedError in the base class. Concrete subclasses in
implementations.py provide the entity-specific conversion logic.

Future work to make this production-ready:
- Replace full-file rewrite with append-only log + periodic compaction
- Add file locking for concurrent access (threading.Lock or fcntl)
- Add encryption for sensitive fields (password hashes, grades)
- Switch to SQLite for better query performance
"""

from __future__ import annotations

import json
import os
from typing import Dict, Generic, List, Optional, TypeVar

from repositories.base import Repository

T = TypeVar("T")
ID = TypeVar("ID")


class FileSystemRepository(Repository[T, ID], Generic[T, ID]):
    """
    Abstract filesystem repository backed by a JSON file.

    Subclasses must implement:
        _serialize(entity)   → dict
        _deserialize(data)   → entity
        _get_id(entity)      → str

    All six CRUD methods are implemented here using JSON read/write.
    """

    def __init__(self, file_path: str):
        """
        Args:
            file_path: Path to the JSON storage file
                       (e.g. 'data/students.json').
                       Created automatically if it does not exist.
        """
        self._file_path = file_path
        self._ensure_file_exists()

    # ------------------------------------------------------------------ #
    # Generic CRUD — implemented once for all filesystem repos
    # ------------------------------------------------------------------ #

    def save(self, entity: T) -> None:
        """Serialize entity and write to JSON file (insert or overwrite)."""
        data = self._load_raw()
        entity_id = self._get_id(entity)
        data[entity_id] = self._serialize(entity)
        self._write_raw(data)

    def find_by_id(self, entity_id: ID) -> Optional[T]:
        """Load JSON and deserialize the matching entry, or return None."""
        data = self._load_raw()
        if entity_id not in data:
            return None
        return self._deserialize(data[entity_id])

    def find_all(self) -> List[T]:
        """Load and deserialize all entries from the JSON file."""
        return [self._deserialize(v) for v in self._load_raw().values()]

    def delete(self, entity_id: ID) -> None:
        """Remove entry from JSON file. Raises KeyError if not found."""
        data = self._load_raw()
        if entity_id not in data:
            raise KeyError(f"No entity with id '{entity_id}' found.")
        del data[entity_id]
        self._write_raw(data)

    def exists(self, entity_id: ID) -> bool:
        """Return True if entry exists in JSON file."""
        return entity_id in self._load_raw()

    def count(self) -> int:
        """Return number of entries in JSON file."""
        return len(self._load_raw())

    # ------------------------------------------------------------------ #
    # File I/O helpers
    # ------------------------------------------------------------------ #

    def _ensure_file_exists(self) -> None:
        """Create the file and any parent directories if they don't exist."""
        os.makedirs(os.path.dirname(self._file_path) or ".", exist_ok=True)
        if not os.path.exists(self._file_path):
            self._write_raw({})

    def _load_raw(self) -> Dict[str, dict]:
        """Read and parse the JSON file. Returns empty dict on failure."""
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_raw(self, data: Dict[str, dict]) -> None:
        """Serialise dict to JSON and write to file."""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    # ------------------------------------------------------------------ #
    # Abstract methods — subclasses must implement
    # ------------------------------------------------------------------ #

    def _serialize(self, entity: T) -> dict:
        """
        Convert a domain object to a plain dict for JSON storage.
        Must be implemented by each concrete filesystem repository.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _serialize()"
        )

    def _deserialize(self, data: dict) -> T:
        """
        Convert a plain dict from JSON storage back to a domain object.
        Must be implemented by each concrete filesystem repository.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _deserialize()"
        )

    def _get_id(self, entity: T) -> str:
        """Extract ID from entity — same logic as InMemoryRepository."""
        for attr in ("user_id", "student_id", "lecturer_id", "course_id",
                     "assignment_id", "submission_id", "grade_id",
                     "notification_id", "enrollment_id"):
            if hasattr(entity, attr):
                return getattr(entity, attr)
        raise AttributeError(
            f"Cannot determine ID for {type(entity).__name__}. "
            f"Override _get_id() in the concrete repository."
        )