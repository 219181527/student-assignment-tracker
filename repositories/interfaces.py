"""
repositories/interfaces.py — Entity-Specific Repository Interfaces
Student Assignment Tracker — Assignment 11

Each interface extends the generic Repository[T, str] and adds
domain-specific query methods beyond the standard four CRUD operations.

Design rationale:
- Separating entity interfaces from the base keeps each interface
  focused and prevents a single bloated file.
- Domain-specific finders (e.g. find_by_course, find_by_student)
  are declared here but NOT implemented — storage backends provide
  them. This keeps business logic free of storage concerns.
- All IDs are str throughout this system, so ID is fixed to str.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, List, Optional

from repositories.base import Repository

if TYPE_CHECKING:
    # Imported only during type checking — never at runtime.
    # Prevents circular imports while giving Pylance full type information.
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
# User Repository
# ---------------------------------------------------------------------------

class UserRepository(Repository["User", str]):
    """
    Repository interface for User entities (base type for Student/Lecturer).
    Extends generic CRUD with email-based lookup and role filtering.
    """

    @abstractmethod
    def find_by_email(self, email: str) -> Optional["User"]:
        """
        Find a user by their email address (used during login).

        Args:
            email: The email address to search for.

        Returns:
            The User if found, None otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_role(self, role: str) -> List["User"]:
        """
        Return all users with a given role ('STUDENT' or 'LECTURER').

        Args:
            role: The role string to filter by.

        Returns:
            List of matching User objects.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Student Repository
# ---------------------------------------------------------------------------

class StudentRepository(Repository["Student", str]):
    """
    Repository interface for Student entities.
    Extends generic CRUD with student-number lookup.
    """

    @abstractmethod
    def find_by_student_number(self, student_number: str) -> Optional["Student"]:
        """
        Find a student by their institutional student number.

        Args:
            student_number: The institutional number (e.g. '219181527').

        Returns:
            The Student if found, None otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_course(self, course_id: str) -> List["Student"]:
        """
        Return all students actively enrolled in a given course.

        Args:
            course_id: The course identifier.

        Returns:
            List of enrolled Student objects.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Lecturer Repository
# ---------------------------------------------------------------------------

class LecturerRepository(Repository["Lecturer", str]):
    """
    Repository interface for Lecturer entities.
    Extends generic CRUD with department-based filtering.
    """

    @abstractmethod
    def find_by_department(self, department: str) -> List["Lecturer"]:
        """
        Return all lecturers in a given academic department.

        Args:
            department: The department name (e.g. 'Computer Science').

        Returns:
            List of matching Lecturer objects.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_employee_number(self, employee_number: str) -> Optional["Lecturer"]:
        """
        Find a lecturer by their institutional employee number.

        Args:
            employee_number: The staff number (e.g. 'EMP001').

        Returns:
            The Lecturer if found, None otherwise.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Course Repository
# ---------------------------------------------------------------------------

class CourseRepository(Repository["Course", str]):
    """
    Repository interface for Course entities.
    Extends generic CRUD with code-based lookup and active filtering.
    """

    @abstractmethod
    def find_by_code(self, course_code: str) -> Optional["Course"]:
        """
        Find a course by its short institutional code (e.g. 'CS301').

        Args:
            course_code: The course code string.

        Returns:
            The Course if found, None otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def find_active(self) -> List["Course"]:
        """
        Return all currently active courses.

        Returns:
            List of Course objects where is_active is True.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Assignment Repository
# ---------------------------------------------------------------------------

class AssignmentRepository(Repository["Assignment", str]):
    """
    Repository interface for Assignment entities.
    Extends generic CRUD with course, lecturer, and status filtering.
    """

    @abstractmethod
    def find_by_course(self, course_id: str) -> List["Assignment"]:
        """
        Return all assignments belonging to a given course.

        Args:
            course_id: The course identifier.

        Returns:
            List of Assignment objects for that course.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_lecturer(self, lecturer_id: str) -> List["Assignment"]:
        """
        Return all assignments created by a given lecturer.

        Args:
            lecturer_id: The lecturer's user ID.

        Returns:
            List of Assignment objects created by that lecturer.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_status(self, status: str) -> List["Assignment"]:
        """
        Return all assignments with a given status.

        Args:
            status: One of 'DRAFT', 'PUBLISHED', 'CLOSED'.

        Returns:
            List of matching Assignment objects.
        """
        raise NotImplementedError

    @abstractmethod
    def find_overdue(self) -> List["Assignment"]:
        """
        Return all published assignments whose due date has passed.

        Returns:
            List of overdue Assignment objects.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Submission Repository
# ---------------------------------------------------------------------------

class SubmissionRepository(Repository["Submission", str]):
    """
    Repository interface for Submission entities.
    Extends generic CRUD with student, assignment, and status filtering.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List["Submission"]:
        """
        Return all submissions made by a given student.

        Args:
            student_id: The student's user ID.

        Returns:
            List of Submission objects by that student.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_assignment(self, assignment_id: str) -> List["Submission"]:
        """
        Return all submissions for a given assignment.

        Args:
            assignment_id: The assignment identifier.

        Returns:
            List of Submission objects for that assignment.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_status(self, status: str) -> List["Submission"]:
        """
        Return all submissions with a given status.

        Args:
            status: One of 'SUBMITTED', 'LATE', 'GRADED'.

        Returns:
            List of matching Submission objects.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_student_and_assignment(
        self, student_id: str, assignment_id: str
    ) -> Optional["Submission"]:
        """
        Find the specific submission a student made for an assignment.
        Business rule: one submission per student per assignment.

        Args:
            student_id:    The student's user ID.
            assignment_id: The assignment identifier.

        Returns:
            The Submission if it exists, None otherwise.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Grade Repository
# ---------------------------------------------------------------------------

class GradeRepository(Repository["Grade", str]):
    """
    Repository interface for Grade entities.
    Extends generic CRUD with submission-based lookup.
    """

    @abstractmethod
    def find_by_submission(self, submission_id: str) -> Optional["Grade"]:
        """
        Find the grade assigned to a specific submission.
        Business rule: zero or one grade per submission.

        Args:
            submission_id: The submission identifier.

        Returns:
            The Grade if it exists, None otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_student(self, student_id: str) -> List["Grade"]:
        """
        Return all grades received by a given student across all assignments.

        Args:
            student_id: The student's user ID.

        Returns:
            List of Grade objects for that student.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Notification Repository
# ---------------------------------------------------------------------------

class NotificationRepository(Repository["Notification", str]):
    """
    Repository interface for Notification entities.
    Extends generic CRUD with student and status filtering.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List["Notification"]:
        """
        Return all notifications sent to a given student.

        Args:
            student_id: The student's user ID.

        Returns:
            List of Notification objects for that student.
        """
        raise NotImplementedError

    @abstractmethod
    def find_unread_by_student(self, student_id: str) -> List["Notification"]:
        """
        Return only unread notifications for a given student.

        Args:
            student_id: The student's user ID.

        Returns:
            List of unread Notification objects.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_trigger_type(self, trigger_type: str) -> List["Notification"]:
        """
        Return all notifications of a given trigger type.

        Args:
            trigger_type: One of 'DEADLINE', 'SUBMISSION', 'GRADE'.

        Returns:
            List of matching Notification objects.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Enrollment Repository
# ---------------------------------------------------------------------------

class EnrollmentRepository(Repository["Enrollment", str]):
    """
    Repository interface for Enrollment entities.
    Extends generic CRUD with student, course, and status filtering.
    """

    @abstractmethod
    def find_by_student(self, student_id: str) -> List["Enrollment"]:
        """
        Return all enrollment records for a given student.

        Args:
            student_id: The student's user ID.

        Returns:
            List of Enrollment objects for that student.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_course(self, course_id: str) -> List["Enrollment"]:
        """
        Return all enrollment records for a given course.

        Args:
            course_id: The course identifier.

        Returns:
            List of Enrollment objects for that course.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_student_and_course(
        self, student_id: str, course_id: str
    ) -> Optional["Enrollment"]:
        """
        Find the specific enrollment record linking a student to a course.
        Business rule: one enrollment per student per course.

        Args:
            student_id: The student's user ID.
            course_id:  The course identifier.

        Returns:
            The Enrollment if it exists, None otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_status(self, status: str) -> List["Enrollment"]:
        """
        Return all enrollments with a given status.

        Args:
            status: One of 'ACTIVE', 'DROPPED', 'COMPLETED'.

        Returns:
            List of matching Enrollment objects.
        """
        raise NotImplementedError