"""
repositories/database/stubs.py — Database Repository Stubs
Student Assignment Tracker — Assignment 11, Task 4

PURPOSE: Future-proofing stub. Demonstrates that switching from
in-memory or filesystem storage to a real SQL/NoSQL database
requires only:
  1. Implementing these stub classes
  2. Changing the RepositoryFactory storage_type to "DATABASE"
  — zero changes to domain classes, services, or tests.

DESIGN NOTES — what a real implementation would look like:

SQL (e.g. PostgreSQL via SQLAlchemy):
    def save(self, entity):
        row = self._serialize(entity)
        self._session.merge(StudentModel(**row))
        self._session.commit()

NoSQL (e.g. MongoDB via PyMongo):
    def save(self, entity):
        self._collection.replace_one(
            {"_id": entity.user_id},
            self._serialize(entity),
            upsert=True
        )

Each stub raises NotImplementedError with a clear message explaining
what needs to be implemented. This is intentional — it prevents silent
failures if DATABASE is selected before the implementation is ready.
"""

from __future__ import annotations

from typing import List, Optional

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

_MSG = (
    "Database repositories are not yet implemented. "
    "To implement: install SQLAlchemy (SQL) or PyMongo (NoSQL), "
    "create a connection pool, and replace each NotImplementedError "
    "with the appropriate ORM/driver call. "
    "See repositories/database/stubs.py for design notes."
)


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------

class DatabaseStudentRepository(StudentRepository):
    """Stub — future SQL/NoSQL implementation for Student entities."""

    def save(self, entity) -> None:
        raise NotImplementedError(_MSG)

    def find_by_id(self, entity_id: str):
        raise NotImplementedError(_MSG)

    def find_all(self) -> List:
        raise NotImplementedError(_MSG)

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError(_MSG)

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(_MSG)

    def count(self) -> int:
        raise NotImplementedError(_MSG)

    def find_by_student_number(self, student_number: str):
        raise NotImplementedError(_MSG)

    def find_by_course(self, course_id: str) -> List:
        raise NotImplementedError(_MSG)


# ---------------------------------------------------------------------------
# Lecturer
# ---------------------------------------------------------------------------

class DatabaseLecturerRepository(LecturerRepository):
    """Stub — future SQL/NoSQL implementation for Lecturer entities."""

    def save(self, entity) -> None:
        raise NotImplementedError(_MSG)

    def find_by_id(self, entity_id: str):
        raise NotImplementedError(_MSG)

    def find_all(self) -> List:
        raise NotImplementedError(_MSG)

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError(_MSG)

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(_MSG)

    def count(self) -> int:
        raise NotImplementedError(_MSG)

    def find_by_department(self, department: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_employee_number(self, employee_number: str):
        raise NotImplementedError(_MSG)


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------

class DatabaseCourseRepository(CourseRepository):
    """Stub — future SQL/NoSQL implementation for Course entities."""

    def save(self, entity) -> None:
        raise NotImplementedError(_MSG)

    def find_by_id(self, entity_id: str):
        raise NotImplementedError(_MSG)

    def find_all(self) -> List:
        raise NotImplementedError(_MSG)

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError(_MSG)

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(_MSG)

    def count(self) -> int:
        raise NotImplementedError(_MSG)

    def find_by_code(self, course_code: str):
        raise NotImplementedError(_MSG)

    def find_active(self) -> List:
        raise NotImplementedError(_MSG)


# ---------------------------------------------------------------------------
# Assignment
# ---------------------------------------------------------------------------

class DatabaseAssignmentRepository(AssignmentRepository):
    """Stub — future SQL/NoSQL implementation for Assignment entities."""

    def save(self, entity) -> None:
        raise NotImplementedError(_MSG)

    def find_by_id(self, entity_id: str):
        raise NotImplementedError(_MSG)

    def find_all(self) -> List:
        raise NotImplementedError(_MSG)

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError(_MSG)

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(_MSG)

    def count(self) -> int:
        raise NotImplementedError(_MSG)

    def find_by_course(self, course_id: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_lecturer(self, lecturer_id: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_status(self, status: str) -> List:
        raise NotImplementedError(_MSG)

    def find_overdue(self) -> List:
        raise NotImplementedError(_MSG)


# ---------------------------------------------------------------------------
# Submission
# ---------------------------------------------------------------------------

class DatabaseSubmissionRepository(SubmissionRepository):
    """Stub — future SQL/NoSQL implementation for Submission entities."""

    def save(self, entity) -> None:
        raise NotImplementedError(_MSG)

    def find_by_id(self, entity_id: str):
        raise NotImplementedError(_MSG)

    def find_all(self) -> List:
        raise NotImplementedError(_MSG)

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError(_MSG)

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(_MSG)

    def count(self) -> int:
        raise NotImplementedError(_MSG)

    def find_by_student(self, student_id: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_assignment(self, assignment_id: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_status(self, status: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_student_and_assignment(self, student_id: str, assignment_id: str):
        raise NotImplementedError(_MSG)


# ---------------------------------------------------------------------------
# Grade
# ---------------------------------------------------------------------------

class DatabaseGradeRepository(GradeRepository):
    """Stub — future SQL/NoSQL implementation for Grade entities."""

    def save(self, entity) -> None:
        raise NotImplementedError(_MSG)

    def find_by_id(self, entity_id: str):
        raise NotImplementedError(_MSG)

    def find_all(self) -> List:
        raise NotImplementedError(_MSG)

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError(_MSG)

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(_MSG)

    def count(self) -> int:
        raise NotImplementedError(_MSG)

    def find_by_submission(self, submission_id: str):
        raise NotImplementedError(_MSG)

    def find_by_student(self, student_id: str) -> List:
        raise NotImplementedError(_MSG)


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

class DatabaseNotificationRepository(NotificationRepository):
    """Stub — future SQL/NoSQL implementation for Notification entities."""

    def save(self, entity) -> None:
        raise NotImplementedError(_MSG)

    def find_by_id(self, entity_id: str):
        raise NotImplementedError(_MSG)

    def find_all(self) -> List:
        raise NotImplementedError(_MSG)

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError(_MSG)

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(_MSG)

    def count(self) -> int:
        raise NotImplementedError(_MSG)

    def find_by_student(self, student_id: str) -> List:
        raise NotImplementedError(_MSG)

    def find_unread_by_student(self, student_id: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_trigger_type(self, trigger_type: str) -> List:
        raise NotImplementedError(_MSG)


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

class DatabaseEnrollmentRepository(EnrollmentRepository):
    """Stub — future SQL/NoSQL implementation for Enrollment entities."""

    def save(self, entity) -> None:
        raise NotImplementedError(_MSG)

    def find_by_id(self, entity_id: str):
        raise NotImplementedError(_MSG)

    def find_all(self) -> List:
        raise NotImplementedError(_MSG)

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError(_MSG)

    def exists(self, entity_id: str) -> bool:
        raise NotImplementedError(_MSG)

    def count(self) -> int:
        raise NotImplementedError(_MSG)

    def find_by_student(self, student_id: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_course(self, course_id: str) -> List:
        raise NotImplementedError(_MSG)

    def find_by_student_and_course(self, student_id: str, course_id: str):
        raise NotImplementedError(_MSG)

    def find_by_status(self, status: str) -> List:
        raise NotImplementedError(_MSG)