"""
repositories/filesystem/implementations.py — FileSystem Repository Implementations
Student Assignment Tracker — Assignment 11, Task 4

Concrete JSON-backed repositories, one per domain entity.
Each class:
  1. Inherits CRUD from FileSystemRepository (reads/writes JSON)
  2. Implements _serialize() / _deserialize() for its entity type
  3. Implements entity-specific finders (same signatures as interfaces.py)
     by loading all records and filtering in memory

NOTE: This is a STUB-LEVEL implementation. The serialize/deserialize
methods store only primitive fields (IDs, strings, dates, enums).
Full object graph reconstruction (e.g. re-linking a Submission to its
Assignment object) would require a unit-of-work pattern and is out of
scope for this assignment. The stubs demonstrate the pattern clearly
and are designed to be extended.

Future production steps:
  - Replace in-memory filtering with SQL WHERE clauses or MongoDB queries
  - Add proper object graph reconstruction via a UnitOfWork registry
  - Add schema versioning for JSON file migrations
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from repositories.filesystem.base_filesystem import FileSystemRepository
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

if TYPE_CHECKING:
    from src.student import Student
    from src.lecturer import Lecturer
    from src.course import Course
    from src.assignment import Assignment
    from src.submission import Submission
    from src.grade import Grade
    from src.notification import Notification
    from src.enrollment import Enrollment


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------

class FileSystemStudentRepository(FileSystemRepository, StudentRepository):
    """JSON-backed repository for Student entities."""

    def _serialize(self, entity) -> dict:
        return {
            "user_id":        entity.user_id,
            "name":           entity.name,
            "email":          entity.email,
            "student_number": entity.student_number,
            "year_of_study":  entity.year_of_study,
            "role":           entity.role,
            "is_active":      entity.is_active,
        }

    def _deserialize(self, data: dict):
        from src.student import Student
        s = Student(
            data["user_id"], data["name"], data["email"],
            "__hashed__",       # Password not stored in plaintext
            data["student_number"], data["year_of_study"],
        )
        if data.get("is_active"):
            s.register()
        return s

    def find_by_student_number(self, student_number: str) -> Optional["Student"]:
        return next(
            (s for s in self.find_all() if s.student_number == student_number),
            None,
        )

    def find_by_course(self, course_id: str) -> List["Student"]:
        # Stub — full graph traversal requires UnitOfWork
        # In production: JOIN students ↔ enrollments ↔ courses
        return [
            s for s in self.find_all()
            if any(
                e.course.course_id == course_id and e.status == "ACTIVE"
                for e in s.get_enrollments()
            )
        ]


# ---------------------------------------------------------------------------
# Lecturer
# ---------------------------------------------------------------------------

class FileSystemLecturerRepository(FileSystemRepository, LecturerRepository):
    """JSON-backed repository for Lecturer entities."""

    def _serialize(self, entity) -> dict:
        return {
            "user_id":         entity.user_id,
            "name":            entity.name,
            "email":           entity.email,
            "department":      entity.department,
            "employee_number": entity.employee_number,
            "role":            entity.role,
            "is_active":       entity.is_active,
        }

    def _deserialize(self, data: dict):
        from src.lecturer import Lecturer
        l = Lecturer(
            data["user_id"], data["name"], data["email"],
            "__hashed__",
            data["department"], data["employee_number"],
        )
        if data.get("is_active"):
            l.register()
        return l

    def find_by_department(self, department: str) -> List["Lecturer"]:
        return [
            l for l in self.find_all()
            if l.department.lower() == department.lower()
        ]

    def find_by_employee_number(self, employee_number: str) -> Optional["Lecturer"]:
        return next(
            (l for l in self.find_all()
             if l.employee_number == employee_number),
            None,
        )


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------

class FileSystemCourseRepository(FileSystemRepository, CourseRepository):
    """JSON-backed repository for Course entities."""

    def _serialize(self, entity) -> dict:
        return {
            "course_id":   entity.course_id,
            "course_name": entity.course_name,
            "course_code": entity.course_code,
            "credit_hours": entity.credit_hours,
            "is_active":   entity.is_active,
        }

    def _deserialize(self, data: dict):
        from src.course import Course
        c = Course(
            data["course_id"], data["course_name"],
            data["course_code"], data["credit_hours"],
        )
        if not data.get("is_active", True):
            c.deactivate()
        return c

    def find_by_code(self, course_code: str) -> Optional["Course"]:
        return next(
            (c for c in self.find_all() if c.course_code == course_code),
            None,
        )

    def find_active(self) -> List["Course"]:
        return [c for c in self.find_all() if c.is_active]


# ---------------------------------------------------------------------------
# Assignment
# ---------------------------------------------------------------------------

class FileSystemAssignmentRepository(FileSystemRepository, AssignmentRepository):
    """JSON-backed repository for Assignment entities (stub — partial graph)."""

    def _serialize(self, entity) -> dict:
        return {
            "assignment_id": entity.assignment_id,
            "title":         entity.title,
            "description":   entity.description,
            "due_date":      str(entity.due_date),
            "total_marks":   entity.total_marks,
            "status":        entity.status,
            "course_id":     entity.course.course_id,
            "lecturer_id":   entity._lecturer.user_id,
        }

    def _deserialize(self, data: dict):
        # Stub — returns a lightweight dict proxy; full reconstruction
        # requires a UnitOfWork to re-link Course and Lecturer objects.
        raise NotImplementedError(
            "FileSystemAssignmentRepository._deserialize() requires a "
            "UnitOfWork registry to re-link Course and Lecturer objects. "
            "Use InMemoryAssignmentRepository for full object graph support."
        )

    def find_by_course(self, course_id: str) -> List["Assignment"]:
        raw = [v for v in self._load_raw().values() if v["course_id"] == course_id]
        return raw   # Returns raw dicts — stub level

    def find_by_lecturer(self, lecturer_id: str) -> List["Assignment"]:
        return [v for v in self._load_raw().values() if v["lecturer_id"] == lecturer_id]

    def find_by_status(self, status: str) -> List["Assignment"]:
        return [v for v in self._load_raw().values() if v["status"] == status.upper()]

    def find_overdue(self) -> List["Assignment"]:
        from datetime import date
        today = str(date.today())
        return [
            v for v in self._load_raw().values()
            if v["status"] == "PUBLISHED" and v["due_date"] < today
        ]


# ---------------------------------------------------------------------------
# Submission
# ---------------------------------------------------------------------------

class FileSystemSubmissionRepository(FileSystemRepository, SubmissionRepository):
    """JSON-backed repository for Submission entities (stub — partial graph)."""

    def _serialize(self, entity) -> dict:
        return {
            "submission_id":  entity.submission_id,
            "student_id":     entity.student.user_id,
            "assignment_id":  entity.assignment.assignment_id,
            "submission_date": str(entity.submission_date),
            "file_url":       entity.file_url,
            "status":         entity.status,
        }

    def _deserialize(self, data: dict):
        raise NotImplementedError(
            "FileSystemSubmissionRepository._deserialize() requires a "
            "UnitOfWork registry to re-link Student and Assignment objects."
        )

    def find_by_student(self, student_id: str) -> List:
        return [v for v in self._load_raw().values() if v["student_id"] == student_id]

    def find_by_assignment(self, assignment_id: str) -> List:
        return [v for v in self._load_raw().values() if v["assignment_id"] == assignment_id]

    def find_by_status(self, status: str) -> List:
        return [v for v in self._load_raw().values() if v["status"] == status.upper()]

    def find_by_student_and_assignment(self, student_id: str, assignment_id: str) -> Optional[dict]:
        return next(
            (v for v in self._load_raw().values()
             if v["student_id"] == student_id
             and v["assignment_id"] == assignment_id),
            None,
        )


# ---------------------------------------------------------------------------
# Grade
# ---------------------------------------------------------------------------

class FileSystemGradeRepository(FileSystemRepository, GradeRepository):
    """JSON-backed repository for Grade entities (stub — partial graph)."""

    def _serialize(self, entity) -> dict:
        return {
            "grade_id":      entity.grade_id,
            "submission_id": entity._submission.submission_id,
            "student_id":    entity._submission.student.user_id,
            "score":         entity.score,
            "feedback":      entity.feedback,
            "graded_date":   str(entity.graded_date),
        }

    def _deserialize(self, data: dict):
        raise NotImplementedError(
            "FileSystemGradeRepository._deserialize() requires a "
            "UnitOfWork registry to re-link Submission objects."
        )

    def find_by_submission(self, submission_id: str) -> Optional[dict]:
        return next(
            (v for v in self._load_raw().values()
             if v["submission_id"] == submission_id),
            None,
        )

    def find_by_student(self, student_id: str) -> List:
        return [v for v in self._load_raw().values() if v["student_id"] == student_id]


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

class FileSystemNotificationRepository(FileSystemRepository, NotificationRepository):
    """JSON-backed repository for Notification entities."""

    def _serialize(self, entity) -> dict:
        return {
            "notification_id": entity.notification_id,
            "message":         entity.message,
            "sent_date":       str(entity.sent_date),
            "status":          entity.get_status(),
            "trigger_type":    entity.trigger_type,
            "student_id":      getattr(entity, "_student_id", None),
        }

    def _deserialize(self, data: dict):
        from src.notification import Notification
        n = Notification(
            data["notification_id"],
            data["message"],
            data["trigger_type"],
            source=None,
        )
        if data.get("student_id"):
            n._student_id = data["student_id"]
        if data.get("status") == "READ":
            n.mark_as_read()
        return n

    def find_by_student(self, student_id: str) -> List["Notification"]:
        return [
            n for n in self.find_all()
            if getattr(n, "_student_id", None) == student_id
        ]

    def save(self, entity, student_id: str = None) -> None:
        """Override save to optionally record student_id on the notification."""
        if student_id:
            entity._student_id = student_id
        super().save(entity)

    def find_unread_by_student(self, student_id: str) -> List["Notification"]:
        return [
            n for n in self.find_by_student(student_id)
            if n.get_status() == "UNREAD"
        ]

    def find_by_trigger_type(self, trigger_type: str) -> List["Notification"]:
        return [
            n for n in self.find_all()
            if n.trigger_type == trigger_type.upper()
        ]


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

class FileSystemEnrollmentRepository(FileSystemRepository, EnrollmentRepository):
    """JSON-backed repository for Enrollment entities (stub — partial graph)."""

    def _serialize(self, entity) -> dict:
        return {
            "enrollment_id":   entity.enrollment_id,
            "student_id":      entity.student.user_id,
            "course_id":       entity.course.course_id,
            "enrollment_date": str(entity.enrollment_date),
            "status":          entity.status,
        }

    def _deserialize(self, data: dict):
        raise NotImplementedError(
            "FileSystemEnrollmentRepository._deserialize() requires a "
            "UnitOfWork registry to re-link Student and Course objects."
        )

    def find_by_student(self, student_id: str) -> List:
        return [v for v in self._load_raw().values() if v["student_id"] == student_id]

    def find_by_course(self, course_id: str) -> List:
        return [v for v in self._load_raw().values() if v["course_id"] == course_id]

    def find_by_student_and_course(self, student_id: str, course_id: str) -> Optional[dict]:
        return next(
            (v for v in self._load_raw().values()
             if v["student_id"] == student_id and v["course_id"] == course_id),
            None,
        )

    def find_by_status(self, status: str) -> List:
        return [v for v in self._load_raw().values() if v["status"] == status.upper()]