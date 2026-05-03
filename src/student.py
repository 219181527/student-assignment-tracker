"""
student.py — Student class for Student Assignment Tracker
Extends User. Implements Student entity from Class Diagram (Assignment 9).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List
from src.user import User

if TYPE_CHECKING:
    from src.enrollment import Enrollment
    from src.submission import Submission
    from src.assignment import Assignment
    from src.notification import Notification


class Student(User):
    """
    Represents a learner enrolled in the system.
    Inherits authentication and profile management from User.
    """

    def __init__(self, user_id: str, name: str, email: str, password: str,
                 student_number: str, year_of_study: int):
        super().__init__(user_id, name, email, password, role="STUDENT")
        self._student_number = student_number
        self._year_of_study = year_of_study
        self._enrollments: List = []    # List[Enrollment]
        self._submissions: List = []    # List[Submission]
        self._notifications: List = []  # List[Notification]

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def view_assignments(self, course_id: str) -> List:
        """Return all assignments for a given enrolled course."""
        enrolled_course_ids = [e.course.course_id for e in self._enrollments if e.status == "ACTIVE"]
        if course_id not in enrolled_course_ids:
            raise PermissionError(f"Student is not actively enrolled in course {course_id}.")
        course = next(e.course for e in self._enrollments if e.course.course_id == course_id)
        return course.get_assignments()

    def submit_assignment(self, assignment, file_url: str) -> "Submission":
        """Create and record a new submission for an assignment."""
        from src.submission import Submission
        from datetime import datetime
        submission = Submission(
            submission_id=f"sub_{self._user_id}_{assignment.assignment_id}",
            student=self,
            assignment=assignment,
            submission_date=datetime.now(),
            file_url=file_url
        )
        self._submissions.append(submission)
        assignment.add_submission(submission)
        return submission

    def track_deadlines(self) -> List:
        """Return all assignments with upcoming deadlines across enrolled courses."""
        from datetime import datetime
        upcoming = []
        for enrollment in self._enrollments:
            if enrollment.status == "ACTIVE":
                for assignment in enrollment.course.get_assignments():
                    if assignment.due_date >= datetime.now().date():
                        upcoming.append(assignment)
        return sorted(upcoming, key=lambda a: a.due_date)

    def get_enrollments(self) -> List:
        """Return all enrollment records for this student."""
        return list(self._enrollments)

    def add_enrollment(self, enrollment) -> None:
        """Register an enrollment (called by Enrollment constructor)."""
        self._enrollments.append(enrollment)

    def add_notification(self, notification) -> None:
        """Receive a notification."""
        self._notifications.append(notification)

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    @property
    def student_number(self) -> str:
        return self._student_number

    @property
    def year_of_study(self) -> int:
        return self._year_of_study

    @property
    def notifications(self) -> List:
        return list(self._notifications)