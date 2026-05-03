# conftest.py — shared fixtures for all test modules
import sys, os
sys.path.insert(0, os.path.dirname(__file__) + "/..")

import pytest
from datetime import date, timedelta

from src.student import Student
from src.lecturer import Lecturer
from src.course import Course
from src.enrollment import Enrollment
from src.grade import Grade
from creational_patterns.singleton import NotificationService


# ---------------------------------------------------------------------------
# Core domain fixtures — reused across all test files
# ---------------------------------------------------------------------------

@pytest.fixture
def lecturer():
    l = Lecturer("l1", "Dr Nkosi", "nkosi@uni.ac.za", "securepass", "Computer Science", "EMP001")
    l.register()
    return l


@pytest.fixture
def student():
    s = Student("s1", "Alice Dlamini", "alice@uni.ac.za", "securepass", "219181527", 3)
    s.register()
    return s


@pytest.fixture
def student_b():
    s = Student("s2", "Bob Mokoena", "bob@uni.ac.za", "securepass", "219181528", 2)
    s.register()
    return s


@pytest.fixture
def course():
    return Course("c1", "Software Engineering", "CS301", 15)


@pytest.fixture
def enrolled_student(student, course):
    Enrollment("e1", student, course)
    return student


@pytest.fixture
def assignment(lecturer, course, enrolled_student):
    a = lecturer.create_assignment(
        course,
        title="Domain Model Assignment",
        description="Build a domain model for a given scenario.",
        due_date=date.today() + timedelta(days=7),
        total_marks=100,
    )
    a.publish()
    return a


@pytest.fixture
def submission(enrolled_student, assignment):
    return enrolled_student.submit_assignment(assignment, "https://github.com/student/repo")


@pytest.fixture
def graded_submission(submission, assignment):
    Grade("g1", submission, 82.0, "Well structured.")
    return submission


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset NotificationService state before every test to prevent bleed-over."""
    svc = NotificationService()
    svc.reset_for_testing()
    yield
    svc.reset_for_testing()