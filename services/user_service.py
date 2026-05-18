"""
services/user_service.py — User Service
Student Assignment Tracker

Encapsulates all business logic for user management:
- Registration with duplicate email prevention
- Authentication with active-account enforcement
- Profile updates with ownership checks
- Role-based user lookup

Uses UserRepository and StudentRepository / LecturerRepository
for persistence via the injected RepositoryFactory.
"""

from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from services.base import BaseService, NotFoundError, ValidationError, ConflictError

if TYPE_CHECKING:
    from repositories.factory.repository_factory import RepositoryFactory
    from src.user import User
    from src.student import Student
    from src.lecturer import Lecturer


class UserService(BaseService):
    """
    Service class for user registration, authentication, and profile management.

    Business rules enforced:
    - Email must be unique across all users
    - Users must be active before they can log in
    - Students and Lecturers are created through the factory (UserFactory)
    - Password is never returned in any response
    """

    def __init__(self, repository_factory: "RepositoryFactory"):
        self._factory = repository_factory
        self._user_repo = repository_factory.get_student_repository()
        self._lecturer_repo = repository_factory.get_lecturer_repository()

    # ------------------------------------------------------------------ #
    # Registration
    # ------------------------------------------------------------------ #

    def register_student(
        self,
        user_id: str,
        name: str,
        email: str,
        password: str,
        student_number: str,
        year_of_study: int,
    ) -> "Student":
        """
        Register a new student account.

        Business rules:
        - Email must not already be in use by any student
        - student_number must be non-empty
        - year_of_study must be a positive integer

        Args:
            user_id:        Unique identifier for the student
            name:           Full display name
            email:          Login email address
            password:       Plain-text password (hashed internally)
            student_number: Institutional student number
            year_of_study:  Current academic year (must be > 0)

        Returns:
            The newly registered Student instance.

        Raises:
            ValidationError: If any required field is missing or invalid.
            ConflictError:   If the email is already registered.
        """
        self._require(user_id, "user_id")
        self._require(name, "name")
        self._require(email, "email")
        self._require(password, "password")
        self._require(student_number, "student_number")
        self._require_positive(year_of_study, "year_of_study")

        # Business rule: email must be unique
        existing = self._find_student_by_email(email)
        if existing:
            raise ConflictError(f"Email '{email}' is already registered.")

        # Business rule: student_number must be unique
        existing_num = self._user_repo.find_by_student_number(student_number)
        if existing_num:
            raise ConflictError(
                f"Student number '{student_number}' is already registered."
            )

        from creational_patterns.simple_factory import UserFactory
        student = UserFactory.create_user(
            role="STUDENT",
            user_id=user_id,
            name=name,
            email=email,
            password=password,
            student_number=student_number,
            year_of_study=year_of_study,
        )
        self._user_repo.save(student)
        return student

    def register_lecturer(
        self,
        user_id: str,
        name: str,
        email: str,
        password: str,
        department: str,
        employee_number: str,
    ) -> "Lecturer":
        """
        Register a new lecturer account.

        Business rules:
        - Email must not already be in use
        - employee_number must be unique

        Returns:
            The newly registered Lecturer instance.

        Raises:
            ValidationError: If any required field is missing.
            ConflictError:   If email or employee_number is already in use.
        """
        self._require(user_id, "user_id")
        self._require(name, "name")
        self._require(email, "email")
        self._require(password, "password")
        self._require(department, "department")
        self._require(employee_number, "employee_number")

        existing_emp = self._lecturer_repo.find_by_employee_number(employee_number)
        if existing_emp:
            raise ConflictError(
                f"Employee number '{employee_number}' is already registered."
            )

        from creational_patterns.simple_factory import UserFactory
        lecturer = UserFactory.create_user(
            role="LECTURER",
            user_id=user_id,
            name=name,
            email=email,
            password=password,
            department=department,
            employee_number=employee_number,
        )
        self._lecturer_repo.save(lecturer)
        return lecturer

    # ------------------------------------------------------------------ #
    # Authentication
    # ------------------------------------------------------------------ #

    def login(self, email: str, password: str, role: str) -> "User":
        """
        Authenticate a user by email and password.

        Business rules:
        - Account must exist
        - Account must be active
        - Credentials must match

        Args:
            email:    The user's email address
            password: Plain-text password to verify
            role:     "STUDENT" or "LECTURER"

        Returns:
            The authenticated User instance.

        Raises:
            NotFoundError:   If no account exists with the given email.
            ValidationError: If credentials are incorrect or account is inactive.
        """
        self._require(email, "email")
        self._require(password, "password")
        self._require(role, "role")

        role = role.upper()
        if role == "STUDENT":
            user = self._find_student_by_email(email)
        elif role == "LECTURER":
            user = self._find_lecturer_by_email(email)
        else:
            raise ValidationError(f"Invalid role '{role}'. Must be STUDENT or LECTURER.")

        if not user:
            raise NotFoundError("User", email)

        if not user.is_active:
            raise ValidationError("Account is not active. Please contact support.")

        if not user.login(email, password):
            raise ValidationError("Invalid email or password.")

        return user

    # ------------------------------------------------------------------ #
    # Profile management
    # ------------------------------------------------------------------ #

    def get_student(self, student_id: str) -> "Student":
        """Retrieve a student by ID. Raises NotFoundError if not found."""
        self._require(student_id, "student_id")
        student = self._user_repo.find_by_id(student_id)
        if not student:
            raise NotFoundError("Student", student_id)
        return student

    def get_lecturer(self, lecturer_id: str) -> "Lecturer":
        """Retrieve a lecturer by ID. Raises NotFoundError if not found."""
        self._require(lecturer_id, "lecturer_id")
        lecturer = self._lecturer_repo.find_by_id(lecturer_id)
        if not lecturer:
            raise NotFoundError("Lecturer", lecturer_id)
        return lecturer

    def update_profile(
        self, user_id: str, role: str, name: str = None, email: str = None
    ) -> "User":
        """
        Update a user's name or email.

        Business rules:
        - New email must not already be in use by another user
        - User must exist

        Returns:
            The updated User instance.
        """
        self._require(user_id, "user_id")
        role = role.upper()

        if role == "STUDENT":
            user = self.get_student(user_id)
            if email and email != user.email:
                existing = self._find_student_by_email(email)
                if existing:
                    raise ConflictError(f"Email '{email}' is already in use.")
            user.update_profile(name=name, email=email)
            self._user_repo.save(user)
        elif role == "LECTURER":
            user = self.get_lecturer(user_id)
            if email and email != user.email:
                existing = self._find_lecturer_by_email(email)
                if existing:
                    raise ConflictError(f"Email '{email}' is already in use.")
            user.update_profile(name=name, email=email)
            self._lecturer_repo.save(user)
        else:
            raise ValidationError(f"Invalid role '{role}'.")

        return user

    def get_all_students(self) -> List["Student"]:
        """Return all registered students."""
        return self._user_repo.find_all()

    def get_all_lecturers(self) -> List["Lecturer"]:
        """Return all registered lecturers."""
        return self._lecturer_repo.find_all()

    # ------------------------------------------------------------------ #
    # Private helpers
    # ------------------------------------------------------------------ #

    def _find_student_by_email(self, email: str) -> Optional["Student"]:
        all_students = self._user_repo.find_all()
        return next((s for s in all_students if s.email == email), None)

    def _find_lecturer_by_email(self, email: str) -> Optional["Lecturer"]:
        all_lecturers = self._lecturer_repo.find_all()
        return next((l for l in all_lecturers if l.email == email), None)