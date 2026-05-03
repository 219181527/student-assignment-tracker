"""
creational_patterns/__init__.py
Student Assignment Tracker — Creational Design Patterns
"""

from creational_patterns.simple_factory import UserFactory
from creational_patterns.factory_method import (
    NotificationCreator,
    DeadlineNotificationCreator,
    SubmissionNotificationCreator,
    GradeNotificationCreator,
)
from creational_patterns.abstract_factory import (
    DashboardFactory,
    StudentDashboardFactory,
    LecturerDashboardFactory,
)
from creational_patterns.builder import (
    AssignmentBuilder,
    ConcreteAssignmentBuilder,
    AssignmentDirector,
)
from creational_patterns.prototype import (
    AssignmentTemplate,
    AssignmentTemplateRegistry,
)
from creational_patterns.singleton import NotificationService

__all__ = [
    "UserFactory",
    "NotificationCreator",
    "DeadlineNotificationCreator",
    "SubmissionNotificationCreator",
    "GradeNotificationCreator",
    "DashboardFactory",
    "StudentDashboardFactory",
    "LecturerDashboardFactory",
    "AssignmentBuilder",
    "ConcreteAssignmentBuilder",
    "AssignmentDirector",
    "AssignmentTemplate",
    "AssignmentTemplateRegistry",
    "NotificationService",
]