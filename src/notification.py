"""
notification.py — Notification class for Student Assignment Tracker
Implements Notification entity from Class Diagram (Assignment 9).
"""

from datetime import datetime


class Notification:
    """
    Represents a system-generated alert sent to a student.
    Triggered by Assignment (DEADLINE) or Submission (SUBMISSION, GRADE) events.
    """

    VALID_TRIGGER_TYPES = ("DEADLINE", "SUBMISSION", "GRADE")
    VALID_STATUSES = ("UNREAD", "READ")

    def __init__(self, notification_id: str, message: str,
                 trigger_type: str, source):
        if trigger_type not in self.VALID_TRIGGER_TYPES:
            raise ValueError(f"trigger_type must be one of {self.VALID_TRIGGER_TYPES}.")
        self._notification_id = notification_id
        self._message = message
        self._sent_date = datetime.now()
        self._status = "UNREAD"
        self._trigger_type = trigger_type
        self._source = source  # Assignment or Submission instance

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def send(self, student_id: str) -> None:
        """Mark notification as dispatched (logging hook)."""
        print(f"[Notification] Sent to student {student_id}: {self._message}")

    def mark_as_read(self) -> None:
        """Transition status from UNREAD to READ."""
        self._status = "READ"

    def get_status(self) -> str:
        """Return current read status."""
        return self._status

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    @property
    def notification_id(self) -> str:
        return self._notification_id

    @property
    def message(self) -> str:
        return self._message

    @property
    def sent_date(self) -> datetime:
        return self._sent_date

    @property
    def trigger_type(self) -> str:
        return self._trigger_type

    def __repr__(self) -> str:
        return f"Notification(id={self._notification_id}, type={self._trigger_type}, status={self._status})"