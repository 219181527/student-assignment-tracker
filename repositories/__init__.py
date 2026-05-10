"""
repositories/__init__.py
Student Assignment Tracker — Repository Layer (Assignment 11)

Public API for the repository package.
Import from here rather than from individual modules:

    from repositories import UserRepository, AssignmentRepository
    from repositories.inmemory import InMemoryUserRepository
    from repositories.factory import RepositoryFactory
"""

from repositories.base import Repository
from repositories.interfaces import (
    UserRepository,
    StudentRepository,
    LecturerRepository,
    CourseRepository,
    AssignmentRepository,
    SubmissionRepository,
    GradeRepository,
    NotificationRepository,
    EnrollmentRepository,
)

__all__ = [
    "Repository",
    "UserRepository",
    "StudentRepository",
    "LecturerRepository",
    "CourseRepository",
    "AssignmentRepository",
    "SubmissionRepository",
    "GradeRepository",
    "NotificationRepository",
    "EnrollmentRepository",
]