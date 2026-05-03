"""
user.py — Base User class for Student Assignment Tracker
Implements the User entity from the Class Diagram (Assignment 9).
"""

from datetime import datetime


class User:
    """
    Base class representing any authenticated system user.
    Subclassed by Student and Lecturer.
    """

    def __init__(self, user_id: str, name: str, email: str, password: str, role: str):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._password_hash = self._hash_password(password)
        self._role = role          # "STUDENT" | "LECTURER"
        self._is_active = False    # Requires explicit activation via register()

    # ------------------------------------------------------------------ #
    # Private helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _hash_password(password: str) -> str:
        """Simulate password hashing (use bcrypt in production)."""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def register(self) -> "User":
        """Activate the account after registration."""
        if not self._email or not self._name:
            raise ValueError("Name and email are required to register.")
        self._is_active = True
        return self

    def login(self, email: str, password: str) -> bool:
        """Verify credentials and return True if valid."""
        if not self._is_active:
            raise PermissionError("Account is not active.")
        return self._email == email and self._password_hash == self._hash_password(password)

    def logout(self) -> None:
        """Log the user out (session invalidation handled externally)."""
        pass  # Session state managed at application layer

    def update_profile(self, name: str = None, email: str = None) -> None:
        """Update mutable profile fields."""
        if name:
            self._name = name
        if email:
            self._email = email

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self) -> str:
        return self._role

    @property
    def is_active(self) -> bool:
        return self._is_active

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._user_id}, name={self._name}, role={self._role})"