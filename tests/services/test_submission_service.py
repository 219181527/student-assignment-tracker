"""
tests/services/test_submission_service.py — SubmissionService Unit Tests
Student Assignment Tracker
"""

import pytest
from services.base import (
    NotFoundError, ValidationError, ConflictError, PermissionError
)
from src.grade import Grade


class TestSubmission:

    def test_submit_assignment_returns_submission(
        self, submission_service, enrolled_student, published_assignment
    ):
        sub = submission_service.submit_assignment(
            "s1", published_assignment.assignment_id,
            "https://github.com/s/repo"
        )
        assert sub is not None

    def test_submission_status_is_submitted(
        self, submission_service, enrolled_student, published_assignment
    ):
        sub = submission_service.submit_assignment(
            "s1", published_assignment.assignment_id,
            "https://github.com/s/repo"
        )
        assert sub.status in ("SUBMITTED", "LATE")

    def test_submit_nonexistent_student_raises_not_found(
        self, submission_service, published_assignment
    ):
        with pytest.raises(NotFoundError):
            submission_service.submit_assignment(
                "s_missing", published_assignment.assignment_id,
                "https://github.com/s/repo"
            )

    def test_submit_nonexistent_assignment_raises_not_found(
        self, submission_service, enrolled_student
    ):
        with pytest.raises(NotFoundError):
            submission_service.submit_assignment(
                "s1", "a_missing", "https://github.com/s/repo"
            )

    def test_submit_to_draft_assignment_raises_validation(
        self, submission_service, enrolled_student,
        assignment_service, registered_lecturer, active_course
    ):
        from datetime import date, timedelta
        draft = assignment_service.create_assignment(
            "l1", "c1", "Draft", "Desc",
            date.today() + timedelta(days=5), 100
        )
        with pytest.raises(ValidationError, match="DRAFT"):
            submission_service.submit_assignment(
                "s1", draft.assignment_id, "https://github.com/s/repo"
            )

    def test_submit_to_closed_assignment_raises_validation(
        self, submission_service, enrolled_student,
        published_assignment, assignment_service
    ):
        assignment_service.close_assignment(
            published_assignment.assignment_id, "l1"
        )
        with pytest.raises(ValidationError, match="CLOSED"):
            submission_service.submit_assignment(
                "s1", published_assignment.assignment_id,
                "https://github.com/s/repo"
            )

    def test_submit_without_enrollment_raises_permission(
        self, submission_service, user_service, published_assignment
    ):
        user_service.register_student(
            "s_notenrolled", "Bob", "bob@uni.ac.za", "pass", "STU999", 1
        )
        with pytest.raises(PermissionError, match="not actively enrolled"):
            submission_service.submit_assignment(
                "s_notenrolled", published_assignment.assignment_id,
                "https://github.com/s/repo"
            )

    def test_submit_twice_raises_conflict(
        self, submission_service, enrolled_student, published_assignment
    ):
        submission_service.submit_assignment(
            "s1", published_assignment.assignment_id,
            "https://github.com/s/repo"
        )
        with pytest.raises(ConflictError, match="already submitted"):
            submission_service.submit_assignment(
                "s1", published_assignment.assignment_id,
                "https://github.com/s/repo2"
            )

    def test_empty_file_url_raises_validation(
        self, submission_service, enrolled_student, published_assignment
    ):
        with pytest.raises(ValidationError, match="'file_url'"):
            submission_service.submit_assignment(
                "s1", published_assignment.assignment_id, ""
            )


class TestGrading:

    def test_grade_submission_returns_grade(
        self, submission_service, submission, registered_lecturer
    ):
        grade = submission_service.grade_submission(
            submission.submission_id, "l1", 85.0, "Good work."
        )
        assert isinstance(grade, Grade)

    def test_grade_score_stored_correctly(
        self, submission_service, submission, registered_lecturer
    ):
        grade = submission_service.grade_submission(
            submission.submission_id, "l1", 75.0, "Well done."
        )
        assert grade.score == 75.0

    def test_grade_feedback_stored(
        self, submission_service, submission, registered_lecturer
    ):
        grade = submission_service.grade_submission(
            submission.submission_id, "l1", 90.0, "Excellent."
        )
        assert grade.feedback == "Excellent."

    def test_grade_submission_changes_status_to_graded(
        self, submission_service, submission, registered_lecturer
    ):
        submission_service.grade_submission(
            submission.submission_id, "l1", 80.0, "Good."
        )
        updated_sub = submission_service.get_submission(submission.submission_id)
        assert updated_sub.status == "GRADED"

    def test_grade_already_graded_raises_conflict(
        self, submission_service, submission, registered_lecturer
    ):
        submission_service.grade_submission(
            submission.submission_id, "l1", 80.0, "Good."
        )
        with pytest.raises(ConflictError, match="already been graded"):
            submission_service.grade_submission(
                submission.submission_id, "l1", 70.0, "Updated."
            )

    def test_grade_score_exceeds_total_marks_raises_validation(
        self, submission_service, submission, registered_lecturer
    ):
        with pytest.raises(ValidationError, match="exceeds total marks"):
            submission_service.grade_submission(
                submission.submission_id, "l1", 150.0, "Too high."
            )

    def test_grade_negative_score_raises_validation(
        self, submission_service, submission, registered_lecturer
    ):
        with pytest.raises(ValidationError, match="negative"):
            submission_service.grade_submission(
                submission.submission_id, "l1", -5.0, "Invalid."
            )

    def test_grade_wrong_lecturer_raises_permission(
        self, submission_service, submission, user_service
    ):
        user_service.register_lecturer(
            "l2", "Dr Other", "other@uni.ac.za", "pass", "Math", "EMP002"
        )
        with pytest.raises(PermissionError):
            submission_service.grade_submission(
                submission.submission_id, "l2", 80.0, "Unauthorised."
            )

    def test_grade_nonexistent_submission_raises_not_found(
        self, submission_service, registered_lecturer
    ):
        with pytest.raises(NotFoundError):
            submission_service.grade_submission(
                "sub_missing", "l1", 80.0, "Feedback."
            )


class TestSubmissionRetrieval:

    def test_get_submission_returns_correct(
        self, submission_service, submission
    ):
        result = submission_service.get_submission(submission.submission_id)
        assert result.submission_id == submission.submission_id

    def test_get_submission_not_found_raises(self, submission_service):
        with pytest.raises(NotFoundError):
            submission_service.get_submission("sub_missing")

    def test_get_submissions_for_assignment(
        self, submission_service, submission, published_assignment
    ):
        results = submission_service.get_submissions_for_assignment(
            published_assignment.assignment_id
        )
        assert len(results) == 1

    def test_get_submissions_for_student(
        self, submission_service, submission
    ):
        results = submission_service.get_submissions_for_student("s1")
        assert len(results) == 1

    def test_get_grade_for_submission_before_grading_returns_none(
        self, submission_service, submission
    ):
        result = submission_service.get_grade_for_submission(
            submission.submission_id
        )
        assert result is None

    def test_get_grade_for_submission_after_grading(
        self, submission_service, submission, registered_lecturer
    ):
        submission_service.grade_submission(
            submission.submission_id, "l1", 88.0, "Great."
        )
        grade = submission_service.get_grade_for_submission(
            submission.submission_id
        )
        assert grade is not None
        assert grade.score == 88.0

    def test_get_student_grade_for_assignment_not_submitted_returns_none(
        self, submission_service, enrolled_student, published_assignment
    ):
        result = submission_service.get_student_grade_for_assignment(
            "s1", published_assignment.assignment_id
        )
        assert result is None

    def test_get_student_grade_for_assignment_after_grading(
        self, submission_service, submission,
        registered_lecturer, published_assignment
    ):
        submission_service.grade_submission(
            submission.submission_id, "l1", 92.0, "Excellent work."
        )
        grade = submission_service.get_student_grade_for_assignment(
            "s1", published_assignment.assignment_id
        )
        assert grade.score == 92.0