"""
enrollment.py — Enrollment class for Student Assignment Tracker
Implements Enrollment entity from Class Diagram (Assignment 9).
Resolves the many-to-many between Student and Course.
"""

from datetime import date


class Enrollment:
    """
    Represents the formal registration of a Student in a Course.
    Aggregated by both Student and Course — can exist independently of either.
    Status follows ACTIVE → DROPPED | COMPLETED lifecycle.
    """

    VALID_STATUSES = ("ACTIVE", "DROPPED", "COMPLETED")

    def __init__(self, enrollment_id: str, student, course):
        self._enrollment_id = enrollment_id
        self._student = student
        self._course = course
        self._enrollment_date = date.today()
        self._status = "ACTIVE"
        # Register with both sides of the relationship
        student.add_enrollment(self)
        course.add_enrollment(self)

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def drop(self) -> None:
        """Transition enrollment from ACTIVE to DROPPED."""
        if self._status != "ACTIVE":
            raise ValueError(f"Cannot drop enrollment with status '{self._status}'.")
        self._status = "DROPPED"

    def complete(self) -> None:
        """Transition enrollment from ACTIVE to COMPLETED."""
        if self._status != "ACTIVE":
            raise ValueError(f"Cannot complete enrollment with status '{self._status}'.")
        self._status = "COMPLETED"

    def get_status(self) -> str:
        """Return the current enrollment status."""
        return self._status

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    @property
    def enrollment_id(self) -> str:
        return self._enrollment_id

    @property
    def student(self):
        return self._student

    @property
    def course(self):
        return self._course

    @property
    def enrollment_date(self) -> date:
        return self._enrollment_date

    @property
    def status(self) -> str:
        return self._status

    def __repr__(self) -> str:
        return (f"Enrollment(id={self._enrollment_id}, "
                f"student={self._student.name}, "
                f"course={self._course.course_code}, "
                f"status={self._status})")