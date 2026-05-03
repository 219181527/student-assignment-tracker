"""
tests/test_factory_method.py
Tests for the Factory Method pattern — NotificationCreator subclasses
"""

import pytest
from datetime import date, timedelta

from src.student import Student
from src.lecturer import Lecturer
from src.course import Course
from src.enrollment import Enrollment
from src.grade import Grade
from creational_patterns.factory_method import (
    DeadlineNotificationCreator,
    SubmissionNotificationCreator,
    GradeNotificationCreator,
)


class TestDeadlineNotificationCreator:

    def test_creates_notification_with_deadline_trigger(self, assignment, enrolled_student):
        notif = DeadlineNotificationCreator().notify(enrolled_student, assignment)
        assert notif.trigger_type == "DEADLINE"

    def test_notification_message_contains_assignment_title(self, assignment, enrolled_student):
        notif = DeadlineNotificationCreator().notify(enrolled_student, assignment)
        assert assignment.title in notif.message

    def test_notification_message_contains_due_date(self, assignment, enrolled_student):
        notif = DeadlineNotificationCreator().notify(enrolled_student, assignment)
        assert str(assignment.due_date) in notif.message

    def test_notification_added_to_student(self, assignment, enrolled_student):
        before = len(enrolled_student.notifications)
        DeadlineNotificationCreator().notify(enrolled_student, assignment)
        assert len(enrolled_student.notifications) == before + 1

    def test_notification_is_unread_by_default(self, assignment, enrolled_student):
        notif = DeadlineNotificationCreator().notify(enrolled_student, assignment)
        assert notif.get_status() == "UNREAD"

    def test_notification_id_is_unique_per_student(self, assignment, enrolled_student, student_b, course):
        Enrollment("e2", student_b, course)
        n1 = DeadlineNotificationCreator().notify(enrolled_student, assignment)
        n2 = DeadlineNotificationCreator().notify(student_b, assignment)
        assert n1.notification_id != n2.notification_id


class TestSubmissionNotificationCreator:

    def test_creates_notification_with_submission_trigger(self, submission, enrolled_student):
        notif = SubmissionNotificationCreator().notify(enrolled_student, submission)
        assert notif.trigger_type == "SUBMISSION"

    def test_message_contains_assignment_title(self, submission, enrolled_student):
        notif = SubmissionNotificationCreator().notify(enrolled_student, submission)
        assert submission.assignment.title in notif.message

    def test_message_contains_submission_status(self, submission, enrolled_student):
        notif = SubmissionNotificationCreator().notify(enrolled_student, submission)
        assert submission.status in notif.message

    def test_notification_added_to_student(self, submission, enrolled_student):
        before = len(enrolled_student.notifications)
        SubmissionNotificationCreator().notify(enrolled_student, submission)
        assert len(enrolled_student.notifications) == before + 1


class TestGradeNotificationCreator:

    def test_creates_notification_with_grade_trigger(self, graded_submission, enrolled_student):
        notif = GradeNotificationCreator().notify(enrolled_student, graded_submission)
        assert notif.trigger_type == "GRADE"

    def test_message_contains_score(self, graded_submission, enrolled_student):
        notif = GradeNotificationCreator().notify(enrolled_student, graded_submission)
        grade = graded_submission.get_grade()
        assert str(grade.score) in notif.message

    def test_message_contains_feedback(self, graded_submission, enrolled_student):
        notif = GradeNotificationCreator().notify(enrolled_student, graded_submission)
        assert graded_submission.get_grade().feedback in notif.message

    def test_message_contains_percentage(self, graded_submission, enrolled_student):
        notif = GradeNotificationCreator().notify(enrolled_student, graded_submission)
        # Score 82/100 = 82.0%
        assert "82.0%" in notif.message

    def test_grade_notification_requires_graded_submission(self, submission, enrolled_student):
        """Calling GradeNotificationCreator on an ungraded submission should raise AttributeError."""
        with pytest.raises(AttributeError):
            GradeNotificationCreator().notify(enrolled_student, submission)


class TestFactoryMethodPolymorphism:

    def test_all_creators_produce_notifications(self, assignment, submission, graded_submission, enrolled_student):
        """Each concrete creator produces a valid Notification object."""
        from src.notification import Notification
        n1 = DeadlineNotificationCreator().notify(enrolled_student, assignment)
        n2 = SubmissionNotificationCreator().notify(enrolled_student, submission)
        n3 = GradeNotificationCreator().notify(enrolled_student, graded_submission)
        for n in (n1, n2, n3):
            assert isinstance(n, Notification)

    def test_each_creator_produces_distinct_trigger_types(self, assignment, submission, graded_submission, enrolled_student):
        n1 = DeadlineNotificationCreator().notify(enrolled_student, assignment)
        n2 = SubmissionNotificationCreator().notify(enrolled_student, submission)
        n3 = GradeNotificationCreator().notify(enrolled_student, graded_submission)
        types = {n1.trigger_type, n2.trigger_type, n3.trigger_type}
        assert types == {"DEADLINE", "SUBMISSION", "GRADE"}