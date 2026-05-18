"""
tests/api/test_api.py — API Integration Tests
Student Assignment Tracker

Uses FastAPI's TestClient (backed by httpx) to test all endpoints
end-to-end through the full stack: API → Service → Repository.

Each test class uses a fresh in-memory factory injected via
dependency_overrides, so tests are fully isolated from each other.
"""

import sys
sys.path.insert(0, '.')

import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient

from api.main import app
from api.dependencies import get_factory
from repositories.factory import RepositoryFactory
from src.course import Course
from src.enrollment import Enrollment


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """
    Return a TestClient with a fresh isolated in-memory factory.
    Overrides the app-level factory so each test starts clean.
    """
    factory = RepositoryFactory("MEMORY")

    app.dependency_overrides[get_factory] = lambda: factory
    with TestClient(app) as c:
        yield c, factory
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_client(client):
    """
    TestClient pre-seeded with a lecturer, student, course, and enrollment.
    Returns (test_client, factory, lecturer_id, student_id, course_id).
    """
    c, factory = client

    # Register lecturer
    c.post("/api/users/lecturers", json={
        "user_id": "l1", "name": "Dr Nkosi",
        "email": "nkosi@uni.ac.za", "password": "pass123",
        "department": "Computer Science", "employee_number": "EMP001",
    })

    # Register student
    c.post("/api/users/students", json={
        "user_id": "s1", "name": "Alice",
        "email": "alice@uni.ac.za", "password": "pass123",
        "student_number": "219181527", "year_of_study": 3,
    })

    # Add course + enrollment directly via factory
    course = Course("c1", "Software Engineering", "CS301", 15)
    factory.get_course_repository().save(course)

    from services.user_service import UserService
    student = UserService(factory).get_student("s1")
    enrollment = Enrollment("e1", student, course)
    factory.get_enrollment_repository().save(enrollment)

    return c, factory, "l1", "s1", "c1"


@pytest.fixture
def assignment_id(seeded_client):
    """Create and return a published assignment ID."""
    c, factory, l_id, s_id, c_id = seeded_client
    due = str(date.today() + timedelta(days=7))
    resp = c.post("/api/assignments", json={
        "lecturer_id": l_id, "course_id": c_id,
        "title": "Domain Model", "description": "Build a model.",
        "due_date": due, "total_marks": 100,
    })
    a_id = resp.json()["assignment_id"]
    c.post(f"/api/assignments/{a_id}/publish", json={"lecturer_id": l_id})
    return a_id


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

class TestHealthCheck:

    def test_health_returns_200(self, client):
        c, _ = client
        resp = c.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# User endpoints
# ---------------------------------------------------------------------------

class TestUserEndpoints:

    def test_register_student_201(self, client):
        c, _ = client
        resp = c.post("/api/users/students", json={
            "user_id": "s1", "name": "Alice",
            "email": "alice@uni.ac.za", "password": "pass123",
            "student_number": "219181527", "year_of_study": 3,
        })
        assert resp.status_code == 201
        assert resp.json()["user_id"] == "s1"
        assert resp.json()["role"] == "STUDENT"

    def test_register_student_duplicate_email_409(self, client):
        c, _ = client
        payload = {
            "user_id": "s1", "name": "Alice", "email": "alice@uni.ac.za",
            "password": "pass123", "student_number": "STU001", "year_of_study": 2,
        }
        c.post("/api/users/students", json=payload)
        payload["user_id"] = "s2"
        payload["student_number"] = "STU002"
        resp = c.post("/api/users/students", json=payload)
        assert resp.status_code == 409

    def test_register_lecturer_201(self, client):
        c, _ = client
        resp = c.post("/api/users/lecturers", json={
            "user_id": "l1", "name": "Dr Nkosi",
            "email": "nkosi@uni.ac.za", "password": "pass123",
            "department": "CS", "employee_number": "EMP001",
        })
        assert resp.status_code == 201
        assert resp.json()["department"] == "CS"

    def test_login_student_success(self, client):
        c, _ = client
        c.post("/api/users/students", json={
            "user_id": "s1", "name": "Alice", "email": "alice@uni.ac.za",
            "password": "pass123", "student_number": "STU001", "year_of_study": 2,
        })
        resp = c.post("/api/users/login", json={
            "email": "alice@uni.ac.za", "password": "pass123", "role": "STUDENT",
        })
        assert resp.status_code == 200
        assert resp.json()["user_id"] == "s1"

    def test_login_wrong_password_422(self, client):
        c, _ = client
        c.post("/api/users/students", json={
            "user_id": "s1", "name": "Alice", "email": "alice@uni.ac.za",
            "password": "pass123", "student_number": "STU001", "year_of_study": 2,
        })
        resp = c.post("/api/users/login", json={
            "email": "alice@uni.ac.za", "password": "wrong", "role": "STUDENT",
        })
        assert resp.status_code == 422

    def test_get_student_200(self, client):
        c, _ = client
        c.post("/api/users/students", json={
            "user_id": "s1", "name": "Alice", "email": "alice@uni.ac.za",
            "password": "pass123", "student_number": "STU001", "year_of_study": 2,
        })
        resp = c.get("/api/users/students/s1")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Alice"

    def test_get_student_not_found_404(self, client):
        c, _ = client
        resp = c.get("/api/users/students/s_missing")
        assert resp.status_code == 404

    def test_list_students(self, client):
        c, _ = client
        c.post("/api/users/students", json={
            "user_id": "s1", "name": "Alice", "email": "a@u.ac.za",
            "password": "pass123", "student_number": "S1", "year_of_study": 1,
        })
        resp = c.get("/api/users/students")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_update_student_profile(self, client):
        c, _ = client
        c.post("/api/users/students", json={
            "user_id": "s1", "name": "Alice", "email": "alice@uni.ac.za",
            "password": "pass123", "student_number": "STU001", "year_of_study": 2,
        })
        resp = c.put("/api/users/students/s1", json={"name": "Alice Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Alice Updated"


# ---------------------------------------------------------------------------
# Assignment endpoints
# ---------------------------------------------------------------------------

class TestAssignmentEndpoints:

    def test_create_assignment_201(self, seeded_client):
        c, _, l_id, _, c_id = seeded_client
        resp = c.post("/api/assignments", json={
            "lecturer_id": l_id, "course_id": c_id,
            "title": "Domain Model", "description": "Build it.",
            "due_date": str(date.today() + timedelta(days=7)),
            "total_marks": 100,
        })
        assert resp.status_code == 201
        assert resp.json()["status"] == "DRAFT"

    def test_create_assignment_past_due_date_422(self, seeded_client):
        c, _, l_id, _, c_id = seeded_client
        resp = c.post("/api/assignments", json={
            "lecturer_id": l_id, "course_id": c_id,
            "title": "Late", "description": "Too late.",
            "due_date": str(date.today() - timedelta(days=1)),
            "total_marks": 100,
        })
        assert resp.status_code == 422

    def test_publish_assignment_200(self, seeded_client):
        c, _, l_id, _, c_id = seeded_client
        create = c.post("/api/assignments", json={
            "lecturer_id": l_id, "course_id": c_id,
            "title": "Test", "description": "Desc.",
            "due_date": str(date.today() + timedelta(days=5)),
            "total_marks": 50,
        })
        a_id = create.json()["assignment_id"]
        resp = c.post(f"/api/assignments/{a_id}/publish",
                      json={"lecturer_id": l_id})
        assert resp.status_code == 200
        assert resp.json()["status"] == "PUBLISHED"

    def test_close_assignment_200(self, seeded_client):
        c, _, l_id, _, c_id = seeded_client
        create = c.post("/api/assignments", json={
            "lecturer_id": l_id, "course_id": c_id,
            "title": "Test", "description": "Desc.",
            "due_date": str(date.today() + timedelta(days=5)),
            "total_marks": 50,
        })
        a_id = create.json()["assignment_id"]
        c.post(f"/api/assignments/{a_id}/publish", json={"lecturer_id": l_id})
        resp = c.post(f"/api/assignments/{a_id}/close", json={"lecturer_id": l_id})
        assert resp.status_code == 200
        assert resp.json()["status"] == "CLOSED"

    def test_get_assignment_200(self, seeded_client, assignment_id):
        c, *_ = seeded_client
        resp = c.get(f"/api/assignments/{assignment_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Domain Model"

    def test_get_assignment_not_found_404(self, seeded_client):
        c, *_ = seeded_client
        resp = c.get("/api/assignments/a_missing")
        assert resp.status_code == 404

    def test_list_assignments(self, seeded_client, assignment_id):
        c, *_ = seeded_client
        resp = c.get("/api/assignments")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_list_assignments_by_course(self, seeded_client, assignment_id):
        c, _, l_id, _, c_id = seeded_client
        resp = c.get(f"/api/assignments/course/{c_id}")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_delete_draft_assignment_200(self, seeded_client):
        c, _, l_id, _, c_id = seeded_client
        create = c.post("/api/assignments", json={
            "lecturer_id": l_id, "course_id": c_id,
            "title": "To Delete", "description": "Will be deleted.",
            "due_date": str(date.today() + timedelta(days=5)),
            "total_marks": 30,
        })
        a_id = create.json()["assignment_id"]
        resp = c.delete(f"/api/assignments/{a_id}?lecturer_id={l_id}")
        assert resp.status_code == 200
        assert "deleted" in resp.json()["message"]

    def test_wrong_lecturer_publish_403(self, seeded_client):
        c, factory, l_id, _, c_id = seeded_client
        from services.user_service import UserService
        UserService(factory).register_lecturer(
            "l2", "Dr Other", "other@uni.ac.za", "pass", "Math", "EMP002"
        )
        create = c.post("/api/assignments", json={
            "lecturer_id": l_id, "course_id": c_id,
            "title": "Test", "description": "Desc.",
            "due_date": str(date.today() + timedelta(days=5)),
            "total_marks": 50,
        })
        a_id = create.json()["assignment_id"]
        resp = c.post(f"/api/assignments/{a_id}/publish",
                      json={"lecturer_id": "l2"})
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Submission endpoints
# ---------------------------------------------------------------------------

class TestSubmissionEndpoints:

    def test_submit_assignment_201(self, seeded_client, assignment_id):
        c, _, l_id, s_id, _ = seeded_client
        resp = c.post(
            f"/api/submissions?assignment_id={assignment_id}",
            json={"student_id": s_id, "file_url": "https://github.com/s/repo"},
        )
        assert resp.status_code == 201
        assert resp.json()["student_id"] == s_id

    def test_submit_twice_409(self, seeded_client, assignment_id):
        c, _, l_id, s_id, _ = seeded_client
        c.post(f"/api/submissions?assignment_id={assignment_id}",
               json={"student_id": s_id, "file_url": "https://github.com/s/r1"})
        resp = c.post(f"/api/submissions?assignment_id={assignment_id}",
                      json={"student_id": s_id, "file_url": "https://github.com/s/r2"})
        assert resp.status_code == 409

    def test_submit_not_enrolled_403(self, seeded_client, assignment_id):
        c, factory, _, _, _ = seeded_client
        from services.user_service import UserService
        UserService(factory).register_student(
            "s2", "Bob", "bob@uni.ac.za", "pass", "STU002", 1
        )
        resp = c.post(f"/api/submissions?assignment_id={assignment_id}",
                      json={"student_id": "s2",
                            "file_url": "https://github.com/b/repo"})
        assert resp.status_code == 403

    def test_get_submission_200(self, seeded_client, assignment_id):
        c, _, _, s_id, _ = seeded_client
        create = c.post(f"/api/submissions?assignment_id={assignment_id}",
                        json={"student_id": s_id,
                              "file_url": "https://github.com/s/repo"})
        sub_id = create.json()["submission_id"]
        resp = c.get(f"/api/submissions/{sub_id}")
        assert resp.status_code == 200

    def test_get_submission_not_found_404(self, seeded_client):
        c, *_ = seeded_client
        resp = c.get("/api/submissions/sub_missing")
        assert resp.status_code == 404

    def test_grade_submission_201(self, seeded_client, assignment_id):
        c, _, l_id, s_id, _ = seeded_client
        create = c.post(f"/api/submissions?assignment_id={assignment_id}",
                        json={"student_id": s_id,
                              "file_url": "https://github.com/s/repo"})
        sub_id = create.json()["submission_id"]
        resp = c.post(f"/api/submissions/{sub_id}/grade",
                      json={"lecturer_id": l_id, "score": 85.0,
                            "feedback": "Well done."})
        assert resp.status_code == 201
        assert resp.json()["score"] == 85.0
        assert resp.json()["percentage"] == 85.0

    def test_grade_already_graded_409(self, seeded_client, assignment_id):
        c, _, l_id, s_id, _ = seeded_client
        create = c.post(f"/api/submissions?assignment_id={assignment_id}",
                        json={"student_id": s_id,
                              "file_url": "https://github.com/s/repo"})
        sub_id = create.json()["submission_id"]
        c.post(f"/api/submissions/{sub_id}/grade",
               json={"lecturer_id": l_id, "score": 85.0, "feedback": "Good."})
        resp = c.post(f"/api/submissions/{sub_id}/grade",
                      json={"lecturer_id": l_id, "score": 70.0, "feedback": "Again."})
        assert resp.status_code == 409

    def test_get_grade_before_grading_returns_null(self, seeded_client, assignment_id):
        c, _, _, s_id, _ = seeded_client
        create = c.post(f"/api/submissions?assignment_id={assignment_id}",
                        json={"student_id": s_id,
                              "file_url": "https://github.com/s/repo"})
        sub_id = create.json()["submission_id"]
        resp = c.get(f"/api/submissions/{sub_id}/grade")
        assert resp.status_code == 200
        assert resp.json() is None

    def test_list_submissions_for_assignment(self, seeded_client, assignment_id):
        c, _, _, s_id, _ = seeded_client
        c.post(f"/api/submissions?assignment_id={assignment_id}",
               json={"student_id": s_id, "file_url": "https://github.com/s/r"})
        resp = c.get(f"/api/submissions/assignment/{assignment_id}")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_list_submissions_for_student(self, seeded_client, assignment_id):
        c, _, _, s_id, _ = seeded_client
        c.post(f"/api/submissions?assignment_id={assignment_id}",
               json={"student_id": s_id, "file_url": "https://github.com/s/r"})
        resp = c.get(f"/api/submissions/student/{s_id}")
        assert resp.status_code == 200
        assert len(resp.json()) == 1