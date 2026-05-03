"""
simple_factory.py — Simple Factory Pattern
Student Assignment Tracker

Pattern:  Simple Factory
Use Case: Centralised user creation — the system creates either a Student or
          Lecturer from a single factory method based on a role string.
          Callers never import Student or Lecturer directly; they ask the
          factory for "STUDENT" or "LECTURER" and receive the correct object.

Justification: Registration endpoints receive a role field from a form.
               Using a factory here prevents scattered isinstance() checks
               and keeps object creation in one place.
"""

from src.student import Student
from src.lecturer import Lecturer
from src.user import User


class UserFactory:
    """
    Simple Factory that creates User subclass instances based on role.
    Not a class with state — all logic lives in the static factory method.
    """

    @staticmethod
    def create_user(role: str, user_id: str, name: str, email: str,
                    password: str, **kwargs) -> User:
        """
        Create and return a User subclass based on the role argument.

        Args:
            role:       "STUDENT" or "LECTURER"
            user_id:    Unique identifier
            name:       Full name
            email:      Login email
            password:   Plain-text password (hashed inside User)
            **kwargs:   Role-specific fields:
                        STUDENT  → student_number (str), year_of_study (int)
                        LECTURER → department (str), employee_number (str)

        Returns:
            A registered Student or Lecturer instance.

        Raises:
            ValueError: If role is not recognised.
        """
        role = role.upper()

        if role == "STUDENT":
            student_number = kwargs.get("student_number", "STU000")
            year_of_study = kwargs.get("year_of_study", 1)
            user = Student(user_id, name, email, password,
                           student_number, year_of_study)

        elif role == "LECTURER":
            department = kwargs.get("department", "General")
            employee_number = kwargs.get("employee_number", "EMP000")
            user = Lecturer(user_id, name, email, password,
                            department, employee_number)

        else:
            raise ValueError(
                f"Unknown role '{role}'. Expected 'STUDENT' or 'LECTURER'."
            )

        user.register()
        return user


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    student = UserFactory.create_user(
        role="STUDENT",
        user_id="s1",
        name="Alice Dlamini",
        email="alice@uni.ac.za",
        password="secret",
        student_number="219181527",
        year_of_study=3,
    )
    print(f"Created: {student} | Active: {student.is_active}")

    lecturer = UserFactory.create_user(
        role="LECTURER",
        user_id="l1",
        name="Dr Nkosi",
        email="nkosi@uni.ac.za",
        password="secure",
        department="Computer Science",
        employee_number="EMP042",
    )
    print(f"Created: {lecturer} | Active: {lecturer.is_active}")