"""
tests/test_simple_factory.py
Tests for the Simple Factory pattern — UserFactory
"""

import pytest
from src.student import Student
from src.lecturer import Lecturer
from creational_patterns.simple_factory import UserFactory


class TestUserFactoryStudentCreation:

    def test_creates_student_instance(self):
        user = UserFactory.create_user(
            "STUDENT", "s10", "Alice", "alice@uni.ac.za", "pass",
            student_number="STU010", year_of_study=2,
        )
        assert isinstance(user, Student)

    def test_student_is_active_after_creation(self):
        user = UserFactory.create_user(
            "STUDENT", "s11", "Alice", "alice@uni.ac.za", "pass",
            student_number="STU011", year_of_study=1,
        )
        assert user.is_active is True

    def test_student_role_is_set(self):
        user = UserFactory.create_user(
            "STUDENT", "s12", "Alice", "alice@uni.ac.za", "pass",
        )
        assert user.role == "STUDENT"

    def test_student_number_stored(self):
        user = UserFactory.create_user(
            "STUDENT", "s13", "Alice", "alice@uni.ac.za", "pass",
            student_number="219181527",
        )
        assert user.student_number == "219181527"

    def test_year_of_study_stored(self):
        user = UserFactory.create_user(
            "STUDENT", "s14", "Alice", "alice@uni.ac.za", "pass",
            year_of_study=3,
        )
        assert user.year_of_study == 3

    def test_student_name_and_email(self):
        user = UserFactory.create_user(
            "STUDENT", "s15", "Bob", "bob@uni.ac.za", "pass",
        )
        assert user.name == "Bob"
        assert user.email == "bob@uni.ac.za"


class TestUserFactoryLecturerCreation:

    def test_creates_lecturer_instance(self):
        user = UserFactory.create_user(
            "LECTURER", "l10", "Dr X", "x@uni.ac.za", "pass",
            department="CS", employee_number="EMP010",
        )
        assert isinstance(user, Lecturer)

    def test_lecturer_is_active_after_creation(self):
        user = UserFactory.create_user(
            "LECTURER", "l11", "Dr X", "x@uni.ac.za", "pass",
        )
        assert user.is_active is True

    def test_lecturer_role_is_set(self):
        user = UserFactory.create_user(
            "LECTURER", "l12", "Dr X", "x@uni.ac.za", "pass",
        )
        assert user.role == "LECTURER"

    def test_lecturer_department_stored(self):
        user = UserFactory.create_user(
            "LECTURER", "l13", "Dr X", "x@uni.ac.za", "pass",
            department="Mathematics",
        )
        assert user.department == "Mathematics"

    def test_lecturer_employee_number_stored(self):
        user = UserFactory.create_user(
            "LECTURER", "l14", "Dr X", "x@uni.ac.za", "pass",
            employee_number="EMP999",
        )
        assert user.employee_number == "EMP999"


class TestUserFactoryEdgeCases:

    def test_unknown_role_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown role"):
            UserFactory.create_user("ADMIN", "x1", "X", "x@x.com", "p")

    def test_role_case_insensitive_student(self):
        user = UserFactory.create_user(
            "student", "s20", "Alice", "alice2@uni.ac.za", "pass",
        )
        assert isinstance(user, Student)

    def test_role_case_insensitive_lecturer(self):
        user = UserFactory.create_user(
            "lecturer", "l20", "Dr Y", "y@uni.ac.za", "pass",
        )
        assert isinstance(user, Lecturer)

    def test_empty_role_raises_value_error(self):
        with pytest.raises(ValueError):
            UserFactory.create_user("", "x2", "X", "x@x.com", "p")

    def test_password_is_not_stored_in_plaintext(self):
        user = UserFactory.create_user(
            "STUDENT", "s21", "Alice", "alice3@uni.ac.za", "plaintext_password",
        )
        # Access internal attribute to verify hashing
        assert user._password_hash != "plaintext_password"
        assert len(user._password_hash) == 64  # SHA-256 hex digest length

    def test_two_users_different_ids(self):
        u1 = UserFactory.create_user("STUDENT", "s30", "A", "a@uni.ac.za", "p")
        u2 = UserFactory.create_user("STUDENT", "s31", "B", "b@uni.ac.za", "p")
        assert u1.user_id != u2.user_id