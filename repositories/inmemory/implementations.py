"""
repositories/inmemory/implementations.py — In-Memory Repository Implementations
Student Assignment Tracker — Assignment 11

Nine concrete HashMap-backed repositories, one per domain entity.
Each class:
  1. Inherits all six CRUD methods from InMemoryRepository (free)
  2. Implements only the entity-specific finder methods declared
     in its interface (interfaces.py)

Storage backend: Python dict — O(1) get/set/delete by ID,
equivalent to Java HashMap<String, Entity>.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional
from datetime import date

from repositories.inmemory.base_inmemory import InMemoryRepository
from repositories.interfaces import (
    UserRepository,
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
    from src.user import User
    from src.student import Student
    from src.lecturer import Lecturer
    from src.course import Course
    from src.assignment import Assignment
    from src.submission import Submission
    from src.grade import Grade
    from src.notification import Notification
    from src.enrollment import Enrollment


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class InMemoryUserRepository(InMemoryRepository, UserRepository):
    """In-memory repository for User entities."""

    def find_by_email(self, email: str) -> Optional["User"]:
        """Find a user by email address — used during login."""
        return next(
            (u for u in self._storage.values() if u.email == email),
            None,
        )

    def find_by_role(self, role: str) -> List["User"]:
        """Return all users with the given role ('STUDENT' or 'LECTURER')."""
        return [u for u in self._storage.values() if u.role == role.upper()]


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------

class InMemoryStudentRepository(InMemoryRepository, StudentRepository):
    """In-memory repository for Student entities."""

    def find_by_student_number(self, student_number: str) -> Optional["Student"]:
        """Find a student by their institutional student number."""
        return next(
            (s for s in self._storage.values()
             if s.student_number == student_number),
            None,
        )

    def find_by_course(self, course_id: str) -> List["Student"]:
        """Return all students actively enrolled in a given course."""
        return [
            s for s in self._storage.values()
            if any(
                e.course.course_id == course_id and e.status == "ACTIVE"
                for e in s.get_enrollments()
            )
        ]


# ---------------------------------------------------------------------------
# Lecturer
# ---------------------------------------------------------------------------

class InMemoryLecturerRepository(InMemoryRepository, LecturerRepository):
    """In-memory repository for Lecturer entities."""

    def find_by_department(self, department: str) -> List["Lecturer"]:
        """Return all lecturers in a given academic department."""
        return [
            l for l in self._storage.values()
            if l.department.lower() == department.lower()
        ]

    def find_by_employee_number(self, employee_number: str) -> Optional["Lecturer"]:
        """Find a lecturer by their institutional employee number."""
        return next(
            (l for l in self._storage.values()
             if l.employee_number == employee_number),
            None,
        )


# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------

class InMemoryCourseRepository(InMemoryRepository, CourseRepository):
    """In-memory repository for Course entities."""

    def find_by_code(self, course_code: str) -> Optional["Course"]:
        """Find a course by its short institutional code (e.g. 'CS301')."""
        return next(
            (c for c in self._storage.values()
             if c.course_code == course_code),
            None,
        )

    def find_active(self) -> List["Course"]:
        """Return all currently active courses."""
        return [c for c in self._storage.values() if c.is_active]


# ---------------------------------------------------------------------------
# Assignment
# ---------------------------------------------------------------------------

class InMemoryAssignmentRepository(InMemoryRepository, AssignmentRepository):
    """In-memory repository for Assignment entities."""

    def find_by_course(self, course_id: str) -> List["Assignment"]:
        """Return all assignments belonging to a given course."""
        return [
            a for a in self._storage.values()
            if a.course.course_id == course_id
        ]

    def find_by_lecturer(self, lecturer_id: str) -> List["Assignment"]:
        """Return all assignments created by a given lecturer."""
        return [
            a for a in self._storage.values()
            if a._lecturer.user_id == lecturer_id
        ]

    def find_by_status(self, status: str) -> List["Assignment"]:
        """Return all assignments with a given status."""
        return [
            a for a in self._storage.values()
            if a.status == status.upper()
        ]

    def find_overdue(self) -> List["Assignment"]:
        """Return all published assignments whose due date has passed."""
        return [
            a for a in self._storage.values()
            if a.status == "PUBLISHED" and a.is_overdue()
        ]


# ---------------------------------------------------------------------------
# Submission
# ---------------------------------------------------------------------------

class InMemorySubmissionRepository(InMemoryRepository, SubmissionRepository):
    """In-memory repository for Submission entities."""

    def find_by_student(self, student_id: str) -> List["Submission"]:
        """Return all submissions made by a given student."""
        return [
            s for s in self._storage.values()
            if s.student.user_id == student_id
        ]

    def find_by_assignment(self, assignment_id: str) -> List["Submission"]:
        """Return all submissions for a given assignment."""
        return [
            s for s in self._storage.values()
            if s.assignment.assignment_id == assignment_id
        ]

    def find_by_status(self, status: str) -> List["Submission"]:
        """Return all submissions with a given status."""
        return [
            s for s in self._storage.values()
            if s.status == status.upper()
        ]

    def find_by_student_and_assignment(
        self, student_id: str, assignment_id: str
    ) -> Optional["Submission"]:
        """
        Find the specific submission a student made for an assignment.
        Business rule: one submission per student per assignment.
        """
        return next(
            (s for s in self._storage.values()
             if s.student.user_id == student_id
             and s.assignment.assignment_id == assignment_id),
            None,
        )


# ---------------------------------------------------------------------------
# Grade
# ---------------------------------------------------------------------------

class InMemoryGradeRepository(InMemoryRepository, GradeRepository):
    """In-memory repository for Grade entities."""

    def find_by_submission(self, submission_id: str) -> Optional["Grade"]:
        """Find the grade assigned to a specific submission."""
        return next(
            (g for g in self._storage.values()
             if g._submission.submission_id == submission_id),
            None,
        )

    def find_by_student(self, student_id: str) -> List["Grade"]:
        """Return all grades received by a given student."""
        return [
            g for g in self._storage.values()
            if g._submission.student.user_id == student_id
        ]


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

class InMemoryNotificationRepository(InMemoryRepository, NotificationRepository):
    """In-memory repository for Notification entities."""

    def find_by_student(self, student_id: str) -> List["Notification"]:
        """Return all notifications sent to a given student."""
        return [
            n for n in self._storage.values()
            if hasattr(n, '_student_id') and n._student_id == student_id
        ]

    def find_unread_by_student(self, student_id: str) -> List["Notification"]:
        """Return only unread notifications for a given student."""
        return [
            n for n in self.find_by_student(student_id)
            if n.get_status() == "UNREAD"
        ]

    def find_by_trigger_type(self, trigger_type: str) -> List["Notification"]:
        """Return all notifications of a given trigger type."""
        return [
            n for n in self._storage.values()
            if n.trigger_type == trigger_type.upper()
        ]

    def save(self, entity, student_id: str = None) -> None:
        """
        Override save to optionally record the student_id alongside
        the notification for ownership queries.
        """
        if student_id:
            entity._student_id = student_id
        super().save(entity)


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

class InMemoryEnrollmentRepository(InMemoryRepository, EnrollmentRepository):
    """In-memory repository for Enrollment entities."""

    def find_by_student(self, student_id: str) -> List["Enrollment"]:
        """Return all enrollment records for a given student."""
        return [
            e for e in self._storage.values()
            if e.student.user_id == student_id
        ]

    def find_by_course(self, course_id: str) -> List["Enrollment"]:
        """Return all enrollment records for a given course."""
        return [
            e for e in self._storage.values()
            if e.course.course_id == course_id
        ]

    def find_by_student_and_course(
        self, student_id: str, course_id: str
    ) -> Optional["Enrollment"]:
        """
        Find the specific enrollment linking a student to a course.
        Business rule: one enrollment per student per course.
        """
        return next(
            (e for e in self._storage.values()
             if e.student.user_id == student_id
             and e.course.course_id == course_id),
            None,
        )

    def find_by_status(self, status: str) -> List["Enrollment"]:
        """Return all enrollments with a given status."""
        return [
            e for e in self._storage.values()
            if e.status == status.upper()
        ]