"""
abstract_factory.py — Abstract Factory Pattern
Student Assignment Tracker

Pattern:  Abstract Factory
Use Case: Dashboard component families — Students and Lecturers see
          different views of the same data. An abstract DashboardFactory
          defines the interface for creating related components (assignment
          view, submission summary, notification panel). Two concrete
          factories produce the correct family: StudentDashboardFactory
          and LecturerDashboardFactory.

Justification: If a new role (e.g. "Teaching Assistant") is added later,
               only a new concrete factory is needed — no existing code
               changes. Guarantees that components within a family are
               always compatible with each other.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from abc import ABC, abstractmethod
from typing import List


# ---------------------------------------------------------------------------
# Abstract Products
# ---------------------------------------------------------------------------

class AssignmentView(ABC):
    """Abstract product: how assignments are presented on a dashboard."""

    @abstractmethod
    def render(self, assignments: List) -> str:
        pass


class SubmissionSummary(ABC):
    """Abstract product: how submission data is summarised."""

    @abstractmethod
    def render(self, user) -> str:
        pass


class NotificationPanel(ABC):
    """Abstract product: how notifications are displayed."""

    @abstractmethod
    def render(self, notifications: List) -> str:
        pass


# ---------------------------------------------------------------------------
# Concrete Products — Student family
# ---------------------------------------------------------------------------

class StudentAssignmentView(AssignmentView):
    """Shows upcoming deadlines and submission status for a student."""

    def render(self, assignments: List) -> str:
        if not assignments:
            return "[Student View] No upcoming assignments."
        lines = ["[Student View] Your Assignments:"]
        for a in assignments:
            overdue = " ⚠ OVERDUE" if a.is_overdue() else ""
            lines.append(f"  • {a.title} — Due: {a.due_date} — Status: {a.status}{overdue}")
        return "\n".join(lines)


class StudentSubmissionSummary(SubmissionSummary):
    """Shows a student's own submission statuses."""

    def render(self, user) -> str:
        lines = [f"[Student View] Submissions for {user.name}:"]
        for enrollment in user.get_enrollments():
            for assignment in enrollment.course.get_assignments():
                matching = [s for s in assignment.get_submissions() if s.student == user]
                status = matching[0].status if matching else "NOT SUBMITTED"
                lines.append(f"  • {assignment.title}: {status}")
        return "\n".join(lines) if len(lines) > 1 else "[Student View] No submissions yet."


class StudentNotificationPanel(NotificationPanel):
    """Shows unread notifications for a student."""

    def render(self, notifications: List) -> str:
        unread = [n for n in notifications if n.get_status() == "UNREAD"]
        if not unread:
            return "[Student View] No unread notifications."
        lines = [f"[Student View] {len(unread)} unread notification(s):"]
        for n in unread:
            lines.append(f"  🔔 [{n.trigger_type}] {n.message}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Concrete Products — Lecturer family
# ---------------------------------------------------------------------------

class LecturerAssignmentView(AssignmentView):
    """Shows submission counts and status overview for each assignment."""

    def render(self, assignments: List) -> str:
        if not assignments:
            return "[Lecturer View] No assignments created."
        lines = ["[Lecturer View] Assignment Overview:"]
        for a in assignments:
            count = len(a.get_submissions())
            lines.append(
                f"  • {a.title} — Status: {a.status} — "
                f"Submissions: {count} — Due: {a.due_date}"
            )
        return "\n".join(lines)


class LecturerSubmissionSummary(SubmissionSummary):
    """Shows grading progress across all assignments for a lecturer."""

    def render(self, user) -> str:
        lines = [f"[Lecturer View] Grading Summary for {user.name}:"]
        for assignment in user.assignments:
            submissions = assignment.get_submissions()
            graded = sum(1 for s in submissions if s.get_grade() is not None)
            lines.append(
                f"  • {assignment.title}: {graded}/{len(submissions)} graded"
            )
        return "\n".join(lines) if len(lines) > 1 else "[Lecturer View] No assignments."


class LecturerNotificationPanel(NotificationPanel):
    """Shows a summary of triggered notifications for a lecturer's assignments."""

    def render(self, notifications: List) -> str:
        if not notifications:
            return "[Lecturer View] No notifications sent."
        lines = [f"[Lecturer View] {len(notifications)} notification(s) dispatched:"]
        for n in notifications:
            lines.append(f"  📢 [{n.trigger_type}] {n.message[:60]}...")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Abstract Factory
# ---------------------------------------------------------------------------

class DashboardFactory(ABC):
    """Abstract factory defining the interface for creating dashboard components."""

    @abstractmethod
    def create_assignment_view(self) -> AssignmentView:
        pass

    @abstractmethod
    def create_submission_summary(self) -> SubmissionSummary:
        pass

    @abstractmethod
    def create_notification_panel(self) -> NotificationPanel:
        pass


# ---------------------------------------------------------------------------
# Concrete Factories
# ---------------------------------------------------------------------------

class StudentDashboardFactory(DashboardFactory):
    """Produces the Student family of dashboard components."""

    def create_assignment_view(self) -> AssignmentView:
        return StudentAssignmentView()

    def create_submission_summary(self) -> SubmissionSummary:
        return StudentSubmissionSummary()

    def create_notification_panel(self) -> NotificationPanel:
        return StudentNotificationPanel()


class LecturerDashboardFactory(DashboardFactory):
    """Produces the Lecturer family of dashboard components."""

    def create_assignment_view(self) -> AssignmentView:
        return LecturerAssignmentView()

    def create_submission_summary(self) -> SubmissionSummary:
        return LecturerSubmissionSummary()

    def create_notification_panel(self) -> NotificationPanel:
        return LecturerNotificationPanel()


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

def render_dashboard(factory: DashboardFactory, user, assignments, notifications):
    """Render a full dashboard using the provided factory — role-agnostic client."""
    av = factory.create_assignment_view()
    ss = factory.create_submission_summary()
    np = factory.create_notification_panel()

    print(av.render(assignments))
    print(ss.render(user))
    print(np.render(notifications))


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

    a1 = lecturer.create_assignment(course, "Domain Model", "Build it",
                                    date.today() + timedelta(days=3), 100)
    a1.publish()
    submission = student.submit_assignment(a1, "https://github.com/s/repo")
    Grade("g1", submission, 82.0, "Well done.")

    print("=== STUDENT DASHBOARD ===")
    render_dashboard(StudentDashboardFactory(), student,
                     student.track_deadlines(), student.notifications)

    print("\n=== LECTURER DASHBOARD ===")
    render_dashboard(LecturerDashboardFactory(), lecturer,
                     lecturer.assignments, [])