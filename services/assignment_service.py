"""
services/assignment_service.py — Assignment Service
Student Assignment Tracker

Encapsulates all business logic for assignment management:
- Creation with course and lecturer ownership validation
- Publishing with enrolled-student notification
- Status lifecycle enforcement (DRAFT → PUBLISHED → CLOSED)
- Deadline tracking for enrolled students

Business rules enforced:
- Only the creating lecturer can update or delete their own assignment
- Assignments cannot be published more than once
- Assignments cannot be closed unless published
- Due date must be in the future at creation time
"""

from __future__ import annotations

from datetime import date
from typing import List, TYPE_CHECKING

from services.base import (
    BaseService, NotFoundError, ValidationError,
    ConflictError, PermissionError,
)

if TYPE_CHECKING:
    from repositories.factory.repository_factory import RepositoryFactory
    from src.assignment import Assignment
    from src.course import Course
    from src.lecturer import Lecturer


class AssignmentService(BaseService):
    """
    Service class for the full assignment lifecycle.

    Depends on:
        AssignmentRepository  — persist/retrieve assignments
        CourseRepository      — validate course existence
        LecturerRepository    — validate lecturer ownership
    """

    def __init__(self, repository_factory: "RepositoryFactory"):
        self._factory = repository_factory
        self._assignment_repo = repository_factory.get_assignment_repository()
        self._course_repo = repository_factory.get_course_repository()
        self._lecturer_repo = repository_factory.get_lecturer_repository()

    # ------------------------------------------------------------------ #
    # Creation
    # ------------------------------------------------------------------ #

    def create_assignment(
        self,
        lecturer_id: str,
        course_id: str,
        title: str,
        description: str,
        due_date: date,
        total_marks: int,
    ) -> "Assignment":
        """
        Create a new assignment for a course.

        Business rules:
        - Lecturer must exist
        - Course must exist and be active
        - Due date must be today or in the future
        - Total marks must be > 0

        Args:
            lecturer_id:  ID of the creating lecturer
            course_id:    ID of the target course
            title:        Assignment title
            description:  Full task description
            due_date:     Submission deadline
            total_marks:  Maximum achievable score

        Returns:
            The newly created Assignment in DRAFT status.

        Raises:
            NotFoundError:   If lecturer or course doesn't exist.
            ValidationError: If inputs are invalid.
            ConflictError:   If course is inactive.
        """
        self._require(lecturer_id, "lecturer_id")
        self._require(course_id, "course_id")
        self._require(title, "title")
        self._require(description, "description")
        self._require_not_none(due_date, "due_date")
        self._require_positive(total_marks, "total_marks")

        if due_date < date.today():
            raise ValidationError("Due date must be today or in the future.")

        lecturer = self._lecturer_repo.find_by_id(lecturer_id)
        if not lecturer:
            raise NotFoundError("Lecturer", lecturer_id)

        course = self._course_repo.find_by_id(course_id)
        if not course:
            raise NotFoundError("Course", course_id)

        if not course.is_active:
            raise ConflictError(
                f"Course '{course_id}' is inactive — assignments cannot be added."
            )

        assignment = lecturer.create_assignment(
            course, title, description, due_date, total_marks
        )
        self._assignment_repo.save(assignment)
        return assignment

    # ------------------------------------------------------------------ #
    # Retrieval
    # ------------------------------------------------------------------ #

    def get_assignment(self, assignment_id: str) -> "Assignment":
        """Retrieve an assignment by ID. Raises NotFoundError if missing."""
        self._require(assignment_id, "assignment_id")
        assignment = self._assignment_repo.find_by_id(assignment_id)
        if not assignment:
            raise NotFoundError("Assignment", assignment_id)
        return assignment

    def get_assignments_for_course(self, course_id: str) -> List["Assignment"]:
        """Return all assignments for a given course."""
        self._require(course_id, "course_id")
        course = self._course_repo.find_by_id(course_id)
        if not course:
            raise NotFoundError("Course", course_id)
        return self._assignment_repo.find_by_course(course_id)

    def get_assignments_for_lecturer(self, lecturer_id: str) -> List["Assignment"]:
        """Return all assignments created by a given lecturer."""
        self._require(lecturer_id, "lecturer_id")
        lecturer = self._lecturer_repo.find_by_id(lecturer_id)
        if not lecturer:
            raise NotFoundError("Lecturer", lecturer_id)
        return self._assignment_repo.find_by_lecturer(lecturer_id)

    def get_all_assignments(self) -> List["Assignment"]:
        """Return all assignments across all courses."""
        return self._assignment_repo.find_all()

    def get_overdue_assignments(self) -> List["Assignment"]:
        """Return all published assignments whose due date has passed."""
        return self._assignment_repo.find_overdue()

    # ------------------------------------------------------------------ #
    # Lifecycle — publish and close
    # ------------------------------------------------------------------ #

    def publish_assignment(self, assignment_id: str, lecturer_id: str) -> "Assignment":
        """
        Transition an assignment from DRAFT to PUBLISHED.

        Business rules:
        - Assignment must be in DRAFT status
        - Only the creating lecturer can publish it

        Returns:
            The updated Assignment in PUBLISHED status.

        Raises:
            NotFoundError:  If assignment or lecturer doesn't exist.
            PermissionError: If the lecturer doesn't own the assignment.
            ConflictError:  If the assignment is not in DRAFT status.
        """
        self._require(assignment_id, "assignment_id")
        self._require(lecturer_id, "lecturer_id")

        assignment = self.get_assignment(assignment_id)
        self._assert_lecturer_owns(assignment, lecturer_id)

        if assignment.status != "DRAFT":
            raise ConflictError(
                f"Assignment is '{assignment.status}' — only DRAFT assignments can be published."
            )

        assignment.publish()
        self._assignment_repo.save(assignment)
        return assignment

    def close_assignment(self, assignment_id: str, lecturer_id: str) -> "Assignment":
        """
        Transition an assignment from PUBLISHED to CLOSED.

        Business rules:
        - Assignment must be in PUBLISHED status
        - Only the creating lecturer can close it

        Returns:
            The updated Assignment in CLOSED status.
        """
        self._require(assignment_id, "assignment_id")
        self._require(lecturer_id, "lecturer_id")

        assignment = self.get_assignment(assignment_id)
        self._assert_lecturer_owns(assignment, lecturer_id)

        if assignment.status != "PUBLISHED":
            raise ConflictError(
                f"Assignment is '{assignment.status}' — only PUBLISHED assignments can be closed."
            )

        assignment.close()
        self._assignment_repo.save(assignment)
        return assignment

    # ------------------------------------------------------------------ #
    # Update and Delete
    # ------------------------------------------------------------------ #

    def update_assignment(
        self,
        assignment_id: str,
        lecturer_id: str,
        title: str = None,
        due_date: date = None,
    ) -> "Assignment":
        """
        Update an assignment's title or due date.

        Business rules:
        - Only the creating lecturer can update it
        - New due date (if provided) must be in the future
        - Cannot update a CLOSED assignment

        Returns:
            The updated Assignment instance.
        """
        self._require(assignment_id, "assignment_id")
        self._require(lecturer_id, "lecturer_id")

        assignment = self.get_assignment(assignment_id)
        self._assert_lecturer_owns(assignment, lecturer_id)

        if assignment.status == "CLOSED":
            raise ConflictError("Cannot update a CLOSED assignment.")

        if due_date and due_date < date.today():
            raise ValidationError("New due date must be today or in the future.")

        lecturer = self._lecturer_repo.find_by_id(lecturer_id)
        lecturer.update_assignment(assignment, title=title, due_date=due_date)
        self._assignment_repo.save(assignment)
        return assignment

    def delete_assignment(self, assignment_id: str, lecturer_id: str) -> None:
        """
        Delete a DRAFT assignment.

        Business rules:
        - Only DRAFT assignments can be deleted
        - Only the creating lecturer can delete it

        Raises:
            ConflictError: If the assignment is not in DRAFT status.
        """
        self._require(assignment_id, "assignment_id")
        self._require(lecturer_id, "lecturer_id")

        assignment = self.get_assignment(assignment_id)
        self._assert_lecturer_owns(assignment, lecturer_id)

        if assignment.status != "DRAFT":
            raise ConflictError(
                f"Cannot delete a '{assignment.status}' assignment. "
                f"Only DRAFT assignments can be deleted."
            )

        lecturer = self._lecturer_repo.find_by_id(lecturer_id)
        lecturer.delete_assignment(assignment)
        self._assignment_repo.delete(assignment_id)

    # ------------------------------------------------------------------ #
    # Private helpers
    # ------------------------------------------------------------------ #

    def _assert_lecturer_owns(self, assignment: "Assignment", lecturer_id: str) -> None:
        """Raise PermissionError if the lecturer does not own the assignment."""
        if assignment._lecturer.user_id != lecturer_id:
            raise PermissionError(
                f"Lecturer '{lecturer_id}' does not own assignment '{assignment.assignment_id}'."
            )