"""
src/__init__.py — Student Assignment Tracker source package
"""

from src.user import User
from src.student import Student
from src.lecturer import Lecturer
from src.course import Course
from src.assignment import Assignment
from src.submission import Submission
from src.grade import Grade
from src.notification import Notification
from src.enrollment import Enrollment

__all__ = [
    "User",
    "Student",
    "Lecturer",
    "Course",
    "Assignment",
    "Submission",
    "Grade",
    "Notification",
    "Enrollment",
]