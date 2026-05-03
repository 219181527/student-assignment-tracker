"""
tests/test_abstract_factory.py
Tests for the Abstract Factory pattern — DashboardFactory families
"""

import pytest
from creational_patterns.abstract_factory import (
    StudentDashboardFactory,
    LecturerDashboardFactory,
    StudentAssignmentView,
    LecturerAssignmentView,
    StudentSubmissionSummary,
    LecturerSubmissionSummary,
    StudentNotificationPanel,
    LecturerNotificationPanel,
    render_dashboard,
)


class TestStudentDashboardFactory:

    def test_creates_student_assignment_view(self):
        factory = StudentDashboardFactory()
        assert isinstance(factory.create_assignment_view(), StudentAssignmentView)

    def test_creates_student_submission_summary(self):
        factory = StudentDashboardFactory()
        assert isinstance(factory.create_submission_summary(), StudentSubmissionSummary)

    def test_creates_student_notification_panel(self):
        factory = StudentDashboardFactory()
        assert isinstance(factory.create_notification_panel(), StudentNotificationPanel)

    def test_student_assignment_view_shows_due_date(self, assignment):
        view = StudentDashboardFactory().create_assignment_view()
        output = view.render([assignment])
        assert str(assignment.due_date) in output

    def test_student_assignment_view_shows_title(self, assignment):
        view = StudentDashboardFactory().create_assignment_view()
        output = view.render([assignment])
        assert assignment.title in output

    def test_student_assignment_view_empty_list(self):
        view = StudentDashboardFactory().create_assignment_view()
        output = view.render([])
        assert "No upcoming" in output

    def test_student_notification_panel_shows_unread(self, enrolled_student, assignment):
        from creational_patterns.factory_method import DeadlineNotificationCreator
        DeadlineNotificationCreator().notify(enrolled_student, assignment)
        panel = StudentDashboardFactory().create_notification_panel()
        output = panel.render(enrolled_student.notifications)
        assert "unread" in output.lower()

    def test_student_notification_panel_no_notifications(self):
        panel = StudentDashboardFactory().create_notification_panel()
        output = panel.render([])
        assert "No unread" in output

    def test_student_submission_summary_not_submitted(self, enrolled_student, assignment):
        summary = StudentDashboardFactory().create_submission_summary()
        output = summary.render(enrolled_student)
        assert "NOT SUBMITTED" in output

    def test_student_submission_summary_after_submit(self, enrolled_student, submission):
        summary = StudentDashboardFactory().create_submission_summary()
        output = summary.render(enrolled_student)
        assert "NOT SUBMITTED" not in output


class TestLecturerDashboardFactory:

    def test_creates_lecturer_assignment_view(self):
        factory = LecturerDashboardFactory()
        assert isinstance(factory.create_assignment_view(), LecturerAssignmentView)

    def test_creates_lecturer_submission_summary(self):
        factory = LecturerDashboardFactory()
        assert isinstance(factory.create_submission_summary(), LecturerSubmissionSummary)

    def test_creates_lecturer_notification_panel(self):
        factory = LecturerDashboardFactory()
        assert isinstance(factory.create_notification_panel(), LecturerNotificationPanel)

    def test_lecturer_assignment_view_shows_submission_count(self, lecturer, assignment, submission):
        view = LecturerDashboardFactory().create_assignment_view()
        output = view.render(lecturer.assignments)
        assert "Submissions: 1" in output

    def test_lecturer_assignment_view_shows_status(self, lecturer, assignment):
        view = LecturerDashboardFactory().create_assignment_view()
        output = view.render(lecturer.assignments)
        assert "PUBLISHED" in output

    def test_lecturer_assignment_view_empty(self):
        view = LecturerDashboardFactory().create_assignment_view()
        output = view.render([])
        assert "No assignments" in output

    def test_lecturer_submission_summary_grading_progress(self, lecturer, submission, graded_submission):
        summary = LecturerDashboardFactory().create_submission_summary()
        output = summary.render(lecturer)
        assert "1/1 graded" in output


class TestFactoryFamilyCompatibility:

    def test_student_factory_does_not_produce_lecturer_components(self):
        factory = StudentDashboardFactory()
        assert not isinstance(factory.create_assignment_view(), LecturerAssignmentView)
        assert not isinstance(factory.create_submission_summary(), LecturerSubmissionSummary)
        assert not isinstance(factory.create_notification_panel(), LecturerNotificationPanel)

    def test_render_dashboard_works_with_student_factory(self, enrolled_student, assignment):
        """render_dashboard is role-agnostic — accepts either factory."""
        import io, sys
        captured = io.StringIO()
        sys.stdout = captured
        render_dashboard(
            StudentDashboardFactory(),
            enrolled_student,
            enrolled_student.track_deadlines(),
            enrolled_student.notifications,
        )
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        assert "[Student View]" in output

    def test_render_dashboard_works_with_lecturer_factory(self, lecturer, assignment):
        import io, sys
        captured = io.StringIO()
        sys.stdout = captured
        render_dashboard(
            LecturerDashboardFactory(),
            lecturer,
            lecturer.assignments,
            [],
        )
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        assert "[Lecturer View]" in output