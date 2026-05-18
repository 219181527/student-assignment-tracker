"""
tests/services/test_assignment_service.py — AssignmentService Unit Tests
Student Assignment Tracker
"""

import pytest
from datetime import date, timedelta
from services.base import NotFoundError, ValidationError, ConflictError, PermissionError


class TestAssignmentCreation:

    def test_create_assignment_returns_assignment(
        self, assignment_service, registered_lecturer, active_course
    ):
        a = assignment_service.create_assignment(
            "l1", "c1", "Test", "Description",
            date.today() + timedelta(days=5), 100
        )
        assert a.title == "Test"

    def test_create_assignment_status_is_draft(
        self, assignment_service, registered_lecturer, active_course
    ):
        a = assignment_service.create_assignment(
            "l1", "c1", "Test", "Desc",
            date.today() + timedelta(days=5), 100
        )
        assert a.status == "DRAFT"

    def test_create_assignment_past_due_date_raises_validation(
        self, assignment_service, registered_lecturer, active_course
    ):
        with pytest.raises(ValidationError, match="future"):
            assignment_service.create_assignment(
                "l1", "c1", "Test", "Desc",
                date.today() - timedelta(days=1), 100
            )

    def test_create_assignment_nonexistent_lecturer_raises_not_found(
        self, assignment_service, active_course
    ):
        with pytest.raises(NotFoundError):
            assignment_service.create_assignment(
                "l_missing", "c1", "Test", "Desc",
                date.today() + timedelta(days=5), 100
            )

    def test_create_assignment_nonexistent_course_raises_not_found(
        self, assignment_service, registered_lecturer
    ):
        with pytest.raises(NotFoundError):
            assignment_service.create_assignment(
                "l1", "c_missing", "Test", "Desc",
                date.today() + timedelta(days=5), 100
            )

    def test_create_assignment_zero_marks_raises_validation(
        self, assignment_service, registered_lecturer, active_course
    ):
        with pytest.raises(ValidationError, match="'total_marks'"):
            assignment_service.create_assignment(
                "l1", "c1", "Test", "Desc",
                date.today() + timedelta(days=5), 0
            )

    def test_create_assignment_empty_title_raises_validation(
        self, assignment_service, registered_lecturer, active_course
    ):
        with pytest.raises(ValidationError, match="'title'"):
            assignment_service.create_assignment(
                "l1", "c1", "", "Desc",
                date.today() + timedelta(days=5), 100
            )

    def test_create_assignment_inactive_course_raises_conflict(
        self, assignment_service, factory, registered_lecturer
    ):
        from src.course import Course
        inactive = Course("c_off", "Old Course", "CS000", 10)
        inactive.deactivate()
        factory.get_course_repository().save(inactive)
        with pytest.raises(ConflictError, match="inactive"):
            assignment_service.create_assignment(
                "l1", "c_off", "Test", "Desc",
                date.today() + timedelta(days=5), 100
            )


class TestAssignmentLifecycle:

    def test_publish_assignment_changes_status(
        self, assignment_service, registered_lecturer, active_course
    ):
        a = assignment_service.create_assignment(
            "l1", "c1", "Test", "Desc",
            date.today() + timedelta(days=5), 100
        )
        published = assignment_service.publish_assignment(a.assignment_id, "l1")
        assert published.status == "PUBLISHED"

    def test_publish_already_published_raises_conflict(
        self, assignment_service, published_assignment
    ):
        with pytest.raises(ConflictError, match="PUBLISHED"):
            assignment_service.publish_assignment(
                published_assignment.assignment_id, "l1"
            )

    def test_publish_wrong_lecturer_raises_permission(
        self, assignment_service, registered_lecturer, active_course, user_service
    ):
        user_service.register_lecturer(
            "l2", "Dr Other", "other@uni.ac.za", "pass", "Math", "EMP002"
        )
        a = assignment_service.create_assignment(
            "l1", "c1", "Test", "Desc",
            date.today() + timedelta(days=5), 100
        )
        with pytest.raises(PermissionError):
            assignment_service.publish_assignment(a.assignment_id, "l2")

    def test_close_published_assignment(
        self, assignment_service, published_assignment
    ):
        closed = assignment_service.close_assignment(
            published_assignment.assignment_id, "l1"
        )
        assert closed.status == "CLOSED"

    def test_close_draft_assignment_raises_conflict(
        self, assignment_service, registered_lecturer, active_course
    ):
        a = assignment_service.create_assignment(
            "l1", "c1", "Test", "Desc",
            date.today() + timedelta(days=5), 100
        )
        with pytest.raises(ConflictError, match="DRAFT"):
            assignment_service.close_assignment(a.assignment_id, "l1")

    def test_delete_draft_assignment(
        self, assignment_service, registered_lecturer, active_course
    ):
        a = assignment_service.create_assignment(
            "l1", "c1", "Test", "Desc",
            date.today() + timedelta(days=5), 100
        )
        assignment_service.delete_assignment(a.assignment_id, "l1")
        with pytest.raises(NotFoundError):
            assignment_service.get_assignment(a.assignment_id)

    def test_delete_published_assignment_raises_conflict(
        self, assignment_service, published_assignment
    ):
        with pytest.raises(ConflictError, match="PUBLISHED"):
            assignment_service.delete_assignment(
                published_assignment.assignment_id, "l1"
            )


class TestAssignmentRetrieval:

    def test_get_assignment_returns_correct(
        self, assignment_service, published_assignment
    ):
        a = assignment_service.get_assignment(
            published_assignment.assignment_id
        )
        assert a.title == "Domain Model"

    def test_get_assignment_not_found_raises(self, assignment_service):
        with pytest.raises(NotFoundError):
            assignment_service.get_assignment("a_missing")

    def test_get_assignments_for_course(
        self, assignment_service, registered_lecturer, active_course
    ):
        assignment_service.create_assignment(
            "l1", "c1", "A1", "Desc",
            date.today() + timedelta(days=5), 100
        )
        assignment_service.create_assignment(
            "l1", "c1", "A2", "Desc",
            date.today() + timedelta(days=10), 50
        )
        results = assignment_service.get_assignments_for_course("c1")
        assert len(results) == 2

    def test_get_assignments_for_lecturer(
        self, assignment_service, registered_lecturer, active_course
    ):
        assignment_service.create_assignment(
            "l1", "c1", "A1", "Desc",
            date.today() + timedelta(days=5), 100
        )
        results = assignment_service.get_assignments_for_lecturer("l1")
        assert len(results) == 1

    def test_update_assignment_title(
        self, assignment_service, registered_lecturer, active_course
    ):
        a = assignment_service.create_assignment(
            "l1", "c1", "Old Title", "Desc",
            date.today() + timedelta(days=5), 100
        )
        updated = assignment_service.update_assignment(
            a.assignment_id, "l1", title="New Title"
        )
        assert updated.title == "New Title"

    def test_update_closed_assignment_raises_conflict(
        self, assignment_service, published_assignment
    ):
        assignment_service.close_assignment(
            published_assignment.assignment_id, "l1"
        )
        with pytest.raises(ConflictError, match="CLOSED"):
            assignment_service.update_assignment(
                published_assignment.assignment_id, "l1", title="New"
            )