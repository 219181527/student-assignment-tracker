"""
submission.py — Submission class for Student Assignment Tracker
Implements Submission entity from Class Diagram (Assignment 9).
"""

from datetime import datetime


class Submission:
    """
    Represents a student's response to a specific assignment.
    Owned by Assignment (composition). May own one Grade (composition).
    Status follows SUBMITTED → LATE → GRADED lifecycle.
    """

    def __init__(self, submission_id: str, student, assignment,
                 submission_date: datetime, file_url: str):
        self._submission_id = submission_id
        self._student = student
        self._assignment = assignment
        self._submission_date = submission_date
        self._file_url = file_url
        self._status = "LATE" if self.is_late(assignment.due_date) else "SUBMITTED"
        self._grade = None  # Zero or one Grade (composition)

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def is_late(self, due_date) -> bool:
        """Return True if submitted after the assignment due date."""
        sub_date = self._submission_date.date() if isinstance(self._submission_date, datetime) else self._submission_date
        return sub_date > due_date

    def get_grade(self):
        """Return the associated Grade, or None if not yet graded."""
        return self._grade

    def assign_grade(self, grade) -> None:
        """Associate a grade with this submission (called by Grade constructor)."""
        self._grade = grade
        self._status = "GRADED"
        self._trigger_notification()

    def _trigger_notification(self) -> None:
        """Notify the student that their submission has been graded."""
        from src.notification import Notification
        from datetime import datetime as dt
        notif = Notification(
            notification_id=f"notif_grade_{self._submission_id}",
            message=f"Your submission for '{self._assignment.title}' has been graded.",
            trigger_type="GRADE",
            source=self
        )
        self._student.add_notification(notif)

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    @property
    def submission_id(self) -> str:
        return self._submission_id

    @property
    def student(self):
        return self._student

    @property
    def assignment(self):
        return self._assignment

    @property
    def submission_date(self) -> datetime:
        return self._submission_date

    @property
    def file_url(self) -> str:
        return self._file_url

    @property
    def status(self) -> str:
        return self._status

    def __repr__(self) -> str:
        return f"Submission(id={self._submission_id}, status={self._status})"