"""
repositories/factory/repository_factory.py — Repository Factory
Student Assignment Tracker — Assignment 11, Task 3

Pattern:  Factory Pattern (Storage-Abstraction Mechanism)
Purpose:  Decouple business logic from storage details.
          Callers ask the factory for a repository by name and storage type.
          The factory returns the correct implementation — callers never
          import InMemory*, FileSystem*, or Database* classes directly.

Supported storage types:
  "MEMORY"     — In-memory HashMap (Assignment 11, fully implemented)
  "FILESYSTEM" — JSON file storage (Assignment 11, stub — Task 4)
  "DATABASE"   — SQL/NoSQL backend (future, raises NotImplementedError)

Usage:
    factory = RepositoryFactory(storage_type="MEMORY")
    student_repo = factory.get_student_repository()
    student_repo.save(student)

Design decisions:
- Factory holds one instance of each repository per storage type
  (singleton-per-type pattern) so callers share state across a session.
- Adding a new backend (e.g. MongoRepository) requires only:
    1. A new elif branch in each get_*_repository() method
    2. The new implementation class
  — no existing code changes needed (Open/Closed Principle).
- storage_type is normalised to uppercase so "memory", "Memory",
  and "MEMORY" all work identically.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from repositories.interfaces import (
        StudentRepository,
        LecturerRepository,
        CourseRepository,
        AssignmentRepository,
        SubmissionRepository,
        GradeRepository,
        NotificationRepository,
        EnrollmentRepository,
    )

VALID_STORAGE_TYPES = ("MEMORY", "FILESYSTEM", "DATABASE")


class RepositoryFactory:
    """
    Factory that creates and returns repository implementations
    based on the requested storage backend.

    Instantiate once per application session and reuse — all
    get_*_repository() calls return the same instance for that
    storage type (shared state within the session).
    """

    def __init__(self, storage_type: str = "MEMORY"):
        storage_type = storage_type.upper()
        if storage_type not in VALID_STORAGE_TYPES:
            raise ValueError(
                f"Unknown storage type '{storage_type}'. "
                f"Choose from: {VALID_STORAGE_TYPES}"
            )
        self._storage_type = storage_type
        self._instances: dict = {}  # Cache — one repo instance per type

    # ------------------------------------------------------------------ #
    # Public factory methods — one per domain entity
    # ------------------------------------------------------------------ #

    def get_student_repository(self) -> "StudentRepository":
        return self._get_or_create("student", self._make_student_repo)

    def get_lecturer_repository(self) -> "LecturerRepository":
        return self._get_or_create("lecturer", self._make_lecturer_repo)

    def get_course_repository(self) -> "CourseRepository":
        return self._get_or_create("course", self._make_course_repo)

    def get_assignment_repository(self) -> "AssignmentRepository":
        return self._get_or_create("assignment", self._make_assignment_repo)

    def get_submission_repository(self) -> "SubmissionRepository":
        return self._get_or_create("submission", self._make_submission_repo)

    def get_grade_repository(self) -> "GradeRepository":
        return self._get_or_create("grade", self._make_grade_repo)

    def get_notification_repository(self) -> "NotificationRepository":
        return self._get_or_create("notification", self._make_notification_repo)

    def get_enrollment_repository(self) -> "EnrollmentRepository":
        return self._get_or_create("enrollment", self._make_enrollment_repo)

    @property
    def storage_type(self) -> str:
        return self._storage_type

    # ------------------------------------------------------------------ #
    # Internal helpers — instance cache + creation routing
    # ------------------------------------------------------------------ #

    def _get_or_create(self, key: str, maker):
        """Return cached instance or create and cache a new one."""
        if key not in self._instances:
            self._instances[key] = maker()
        return self._instances[key]

    def _make_student_repo(self):
        if self._storage_type == "MEMORY":
            from repositories.inmemory.implementations import InMemoryStudentRepository
            return InMemoryStudentRepository()
        elif self._storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemStudentRepository
            return FileSystemStudentRepository("data/students.json")
        elif self._storage_type == "DATABASE":
            raise NotImplementedError(
                "DatabaseStudentRepository is not yet implemented. "
                "See repositories/database/ stub in Task 4."
            )

    def _make_lecturer_repo(self):
        if self._storage_type == "MEMORY":
            from repositories.inmemory.implementations import InMemoryLecturerRepository
            return InMemoryLecturerRepository()
        elif self._storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemLecturerRepository
            return FileSystemLecturerRepository("data/lecturers.json")
        elif self._storage_type == "DATABASE":
            raise NotImplementedError("DatabaseLecturerRepository not yet implemented.")

    def _make_course_repo(self):
        if self._storage_type == "MEMORY":
            from repositories.inmemory.implementations import InMemoryCourseRepository
            return InMemoryCourseRepository()
        elif self._storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemCourseRepository
            return FileSystemCourseRepository("data/courses.json")
        elif self._storage_type == "DATABASE":
            raise NotImplementedError("DatabaseCourseRepository not yet implemented.")

    def _make_assignment_repo(self):
        if self._storage_type == "MEMORY":
            from repositories.inmemory.implementations import InMemoryAssignmentRepository
            return InMemoryAssignmentRepository()
        elif self._storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemAssignmentRepository
            return FileSystemAssignmentRepository("data/assignments.json")
        elif self._storage_type == "DATABASE":
            raise NotImplementedError("DatabaseAssignmentRepository not yet implemented.")

    def _make_submission_repo(self):
        if self._storage_type == "MEMORY":
            from repositories.inmemory.implementations import InMemorySubmissionRepository
            return InMemorySubmissionRepository()
        elif self._storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemSubmissionRepository
            return FileSystemSubmissionRepository("data/submissions.json")
        elif self._storage_type == "DATABASE":
            raise NotImplementedError("DatabaseSubmissionRepository not yet implemented.")

    def _make_grade_repo(self):
        if self._storage_type == "MEMORY":
            from repositories.inmemory.implementations import InMemoryGradeRepository
            return InMemoryGradeRepository()
        elif self._storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemGradeRepository
            return FileSystemGradeRepository("data/grades.json")
        elif self._storage_type == "DATABASE":
            raise NotImplementedError("DatabaseGradeRepository not yet implemented.")

    def _make_notification_repo(self):
        if self._storage_type == "MEMORY":
            from repositories.inmemory.implementations import InMemoryNotificationRepository
            return InMemoryNotificationRepository()
        elif self._storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemNotificationRepository
            return FileSystemNotificationRepository("data/notifications.json")
        elif self._storage_type == "DATABASE":
            raise NotImplementedError("DatabaseNotificationRepository not yet implemented.")

    def _make_enrollment_repo(self):
        if self._storage_type == "MEMORY":
            from repositories.inmemory.implementations import InMemoryEnrollmentRepository
            return InMemoryEnrollmentRepository()
        elif self._storage_type == "FILESYSTEM":
            from repositories.filesystem.implementations import FileSystemEnrollmentRepository
            return FileSystemEnrollmentRepository("data/enrollments.json")
        elif self._storage_type == "DATABASE":
            raise NotImplementedError("DatabaseEnrollmentRepository not yet implemented.")

    def __repr__(self) -> str:
        return f"RepositoryFactory(storage_type={self._storage_type!r})"