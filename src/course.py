"""
course.py — Course class for Student Assignment Tracker
Implements Course entity from Class Diagram (Assignment 9).
"""

from typing import List


class Course:
    """
    Represents an academic module or subject.
    Owns assignments (composition) and connects to students via Enrollment (aggregation).
    """

    def __init__(self, course_id: str, course_name: str, course_code: str,
                 credit_hours: int = 15):
        self._course_id = course_id
        self._course_name = course_name
        self._course_code = course_code
        self._credit_hours = credit_hours
        self._is_active = True
        self._assignments: List = []    # Composition — assignments owned by course
        self._enrollments: List = []    # Aggregation — enrollment records

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def add_assignment(self, assignment) -> None:
        """Add an assignment to this course (called by Lecturer.create_assignment)."""
        self._assignments.append(assignment)

    def get_assignments(self) -> List:
        """Return all assignments for this course."""
        return list(self._assignments)

    def get_enrolled_students(self) -> List:
        """Return all actively enrolled students."""
        return [e.student for e in self._enrollments if e.status == "ACTIVE"]

    def add_enrollment(self, enrollment) -> None:
        """Register an enrollment record against this course."""
        self._enrollments.append(enrollment)

    def deactivate(self) -> None:
        """Mark course as inactive — no new enrollments or assignments allowed."""
        self._is_active = False

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    @property
    def course_id(self) -> str:
        return self._course_id

    @property
    def course_name(self) -> str:
        return self._course_name

    @property
    def course_code(self) -> str:
        return self._course_code

    @property
    def credit_hours(self) -> int:
        return self._credit_hours

    @property
    def is_active(self) -> bool:
        return self._is_active

    def __repr__(self) -> str:
        return f"Course(id={self._course_id}, code={self._course_code}, name={self._course_name})"