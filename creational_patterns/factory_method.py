"""
factory_method.py — Factory Method Pattern
Student Assignment Tracker

Pattern:  Factory Method
Use Case: Notification creation — different trigger types (DEADLINE,
          SUBMISSION, GRADE) require subtly different notification
          construction logic. An abstract NotificationCreator defines the
          interface; concrete subclasses decide exactly how to build the
          Notification for their trigger type.

Justification: If notification logic for each trigger type grows (e.g.
               DEADLINE notifications need escalation after 24 hrs),
               each subclass can evolve independently without touching the
               others. Open/Closed Principle applied.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from src.notification import Notification


# ---------------------------------------------------------------------------
# Abstract Creator
# ---------------------------------------------------------------------------

class NotificationCreator(ABC):
    """
    Abstract creator declaring the factory method.
    Subclasses override create_notification() to return the right object.
    """

    def notify(self, student, source) -> Notification:
        """
        Template method: build the notification then deliver it.
        Subclasses customise create_notification(), not this method.
        """
        notification = self.create_notification(student, source)
        notification.send(student.user_id)
        student.add_notification(notification)
        return notification

    @abstractmethod
    def create_notification(self, student, source) -> Notification:
        """Factory method — overridden by each concrete creator."""
        pass


# ---------------------------------------------------------------------------
# Concrete Creators
# ---------------------------------------------------------------------------

class DeadlineNotificationCreator(NotificationCreator):
    """Creates a DEADLINE notification when an assignment is published."""

    def create_notification(self, student, source) -> Notification:
        assignment = source
        return Notification(
            notification_id=f"notif_deadline_{assignment.assignment_id}_{student.user_id}",
            message=(
                f"Reminder: '{assignment.title}' is due on {assignment.due_date}. "
                f"Submit before the deadline to avoid late penalties."
            ),
            trigger_type="DEADLINE",
            source=assignment,
        )


class SubmissionNotificationCreator(NotificationCreator):
    """Creates a SUBMISSION confirmation notification when work is submitted."""

    def create_notification(self, student, source) -> Notification:
        submission = source
        return Notification(
            notification_id=f"notif_sub_{submission.submission_id}_{student.user_id}",
            message=(
                f"Your submission for '{submission.assignment.title}' was received "
                f"on {submission.submission_date.strftime('%Y-%m-%d %H:%M')}. "
                f"Status: {submission.status}."
            ),
            trigger_type="SUBMISSION",
            source=submission,
        )


class GradeNotificationCreator(NotificationCreator):
    """Creates a GRADE release notification when a submission is graded."""

    def create_notification(self, student, source) -> Notification:
        submission = source
        grade = submission.get_grade()
        return Notification(
            notification_id=f"notif_grade_{submission.submission_id}_{student.user_id}",
            message=(
                f"Your submission for '{submission.assignment.title}' has been graded. "
                f"Score: {grade.score}/{submission.assignment.total_marks} "
                f"({grade.get_percentage(submission.assignment.total_marks)}%). "
                f"Feedback: {grade.feedback}"
            ),
            trigger_type="GRADE",
            source=submission,
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from datetime import date, timedelta
    from src.student import Student
    from src.lecturer import Lecturer
    from src.course import Course
    from src.enrollment import Enrollment
    from src.grade import Grade

    lecturer = Lecturer("l1", "Dr Nkosi", "nkosi@uni.ac.za", "pass", "CS", "EMP01")
    lecturer.register()
    student = Student("s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2)
    student.register()
    course = Course("c1", "Software Engineering", "CS301")
    Enrollment("e1", student, course)

    assignment = lecturer.create_assignment(
        course, "Domain Model", "Build a domain model",
        date.today() + timedelta(days=5), 100
    )
    assignment.publish()

    submission = student.submit_assignment(assignment, "https://github.com/student/repo")
    grade = Grade("g1", submission, 78.0, "Good structure, minor gaps.")

    # Use factory method pattern directly
    print("\n--- Factory Method: Notification Types ---")
    DeadlineNotificationCreator().notify(student, assignment)
    SubmissionNotificationCreator().notify(student, submission)
    GradeNotificationCreator().notify(student, submission)
    print(f"Total notifications on student: {len(student.notifications)}")