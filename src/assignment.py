"""
assignment.py — Assignment class for Student Assignment Tracker
Implements Assignment entity from Class Diagram (Assignment 9).
"""

from datetime import date
from typing import List


class Assignment:
    """
    Represents coursework created by a Lecturer for a Course.
    Owns submissions (composition). Status follows DRAFT → PUBLISHED → CLOSED lifecycle.
    """

    VALID_STATUSES = ("DRAFT", "PUBLISHED", "CLOSED")

    def __init__(self, assignment_id: str, title: str, description: str,
                 due_date: date, total_marks: int, lecturer, course):
        self._assignment_id = assignment_id
        self._title = title
        self._description = description
        self._due_date = due_date
        self._total_marks = total_marks
        self._status = "DRAFT"
        self._lecturer = lecturer
        self._course = course
        self._submissions: List = []    # Composition — submissions owned by assignment
        self._notifications: List = []  # Notifications triggered by this assignment

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def publish(self) -> None:
        """Transition assignment from DRAFT to PUBLISHED."""
        if self._status != "DRAFT":
            raise ValueError(f"Cannot publish assignment with status '{self._status}'.")
        self._status = "PUBLISHED"
        self._trigger_notification("DEADLINE")

    def close(self) -> None:
        """Transition assignment from PUBLISHED to CLOSED."""
        if self._status != "PUBLISHED":
            raise ValueError(f"Cannot close assignment with status '{self._status}'.")
        self._status = "CLOSED"

    def add_submission(self, submission) -> None:
        """Record a submission against this assignment (called by Student.submit_assignment)."""
        if self._status != "PUBLISHED":
            raise ValueError("Submissions only accepted for PUBLISHED assignments.")
        self._submissions.append(submission)

    def get_submissions(self) -> List:
        """Return all submissions for this assignment."""
        return list(self._submissions)

    def is_overdue(self) -> bool:
        """Return True if the due date has passed."""
        return date.today() > self._due_date

    def _trigger_notification(self, trigger_type: str) -> None:
        """Create a notification linked to this assignment."""
        from src.notification import Notification
        from datetime import datetime
        enrolled_students = self._course.get_enrolled_students()
        for student in enrolled_students:
            msg = f"Assignment '{self._title}' is now published. Due: {self._due_date}."
            notif = Notification(
                notification_id=f"notif_{self._assignment_id}_{student.user_id}",
                message=msg,
                trigger_type=trigger_type,
                source=self
            )
            self._notifications.append(notif)
            student.add_notification(notif)

    # ------------------------------------------------------------------ #
    # Getters / Setters
    # ------------------------------------------------------------------ #

    @property
    def assignment_id(self) -> str:
        return self._assignment_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def description(self) -> str:
        return self._description

    @property
    def due_date(self) -> date:
        return self._due_date

    @due_date.setter
    def due_date(self, value: date) -> None:
        self._due_date = value

    @property
    def total_marks(self) -> int:
        return self._total_marks

    @property
    def status(self) -> str:
        return self._status

    @property
    def course(self):
        return self._course

    def __repr__(self) -> str:
        return f"Assignment(id={self._assignment_id}, title={self._title}, status={self._status})"