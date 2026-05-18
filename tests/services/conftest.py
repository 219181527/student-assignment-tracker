# tests/services/conftest.py — shared fixtures for service tests
import sys
sys.path.insert(0, '.')

import pytest
from datetime import date, timedelta
from repositories.factory import RepositoryFactory
from services.user_service import UserService
from services.assignment_service import AssignmentService
from services.submission_service import SubmissionService
from src.course import Course
from src.enrollment import Enrollment


@pytest.fixture
def factory():
    """Fresh in-memory factory for each test — fully isolated."""
    return RepositoryFactory("MEMORY")


@pytest.fixture
def user_service(factory):
    return UserService(factory)


@pytest.fixture
def assignment_service(factory):
    return AssignmentService(factory)


@pytest.fixture
def submission_service(factory):
    return SubmissionService(factory)


@pytest.fixture
def registered_student(user_service):
    return user_service.register_student(
        user_id="s1", name="Alice Dlamini",
        email="alice@uni.ac.za", password="pass123",
        student_number="219181527", year_of_study=3,
    )


@pytest.fixture
def registered_lecturer(user_service):
    return user_service.register_lecturer(
        user_id="l1", name="Dr Nkosi",
        email="nkosi@uni.ac.za", password="pass123",
        department="Computer Science", employee_number="EMP001",
    )


@pytest.fixture
def active_course(factory):
    course = Course("c1", "Software Engineering", "CS301", 15)
    factory.get_course_repository().save(course)
    return course


@pytest.fixture
def enrolled_student(factory, registered_student, active_course):
    """Student registered AND actively enrolled in active_course."""
    enrollment = Enrollment("e1", registered_student, active_course)
    factory.get_enrollment_repository().save(enrollment)
    return registered_student


@pytest.fixture
def published_assignment(assignment_service, registered_lecturer, active_course):
    assignment = assignment_service.create_assignment(
        lecturer_id="l1",
        course_id="c1",
        title="Domain Model",
        description="Build a domain model.",
        due_date=date.today() + timedelta(days=7),
        total_marks=100,
    )
    assignment_service.publish_assignment(assignment.assignment_id, "l1")
    return assignment


@pytest.fixture
def submission(submission_service, enrolled_student, published_assignment):
    return submission_service.submit_assignment(
        student_id="s1",
        assignment_id=published_assignment.assignment_id,
        file_url="https://github.com/student/repo",
    )