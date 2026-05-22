"""
tests/services/test_user_service.py — UserService Unit Tests
Student Assignment Tracker
"""

import pytest
from services.user_service import UserService
from services.base import NotFoundError, ValidationError, ConflictError
from src.student import Student
from src.lecturer import Lecturer


class TestStudentRegistration:

    def test_register_student_returns_student_instance(self, user_service):
        s = user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2
        )
        assert isinstance(s, Student)

    def test_register_student_is_active(self, user_service):
        s = user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2
        )
        assert s.is_active is False

    def test_register_student_stores_correct_name(self, user_service):
        s = user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2
        )
        assert s.name == "Alice"

    def test_register_student_stores_student_number(self, user_service):
        s = user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "219181527", 3
        )
        assert s.student_number == "219181527"

    def test_register_student_duplicate_email_raises_conflict(self, user_service):
        user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2
        )
        with pytest.raises(ConflictError, match="already registered"):
            user_service.register_student(
                "s2", "Bob", "alice@uni.ac.za", "pass", "STU002", 1
            )

    def test_register_student_duplicate_student_number_raises_conflict(self, user_service):
        user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2
        )
        with pytest.raises(ConflictError, match="already registered"):
            user_service.register_student(
                "s2", "Bob", "bob@uni.ac.za", "pass", "STU001", 1
            )

    def test_register_student_empty_name_raises_validation(self, user_service):
        with pytest.raises(ValidationError, match="'name'"):
            user_service.register_student(
                "s1", "", "alice@uni.ac.za", "pass", "STU001", 2
            )

    def test_register_student_empty_email_raises_validation(self, user_service):
        with pytest.raises(ValidationError, match="'email'"):
            user_service.register_student(
                "s1", "Alice", "", "pass", "STU001", 2
            )

    def test_register_student_zero_year_raises_validation(self, user_service):
        with pytest.raises(ValidationError, match="'year_of_study'"):
            user_service.register_student(
                "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 0
            )

    def test_register_student_negative_year_raises_validation(self, user_service):
        with pytest.raises(ValidationError, match="'year_of_study'"):
            user_service.register_student(
                "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", -1
            )


class TestLecturerRegistration:

    def test_register_lecturer_returns_lecturer_instance(self, user_service):
        l = user_service.register_lecturer(
            "l1", "Dr Nkosi", "nkosi@uni.ac.za", "pass", "CS", "EMP001"
        )
        assert isinstance(l, Lecturer)

    def test_register_lecturer_is_active(self, user_service):
        l = user_service.register_lecturer(
            "l1", "Dr Nkosi", "nkosi@uni.ac.za", "pass", "CS", "EMP001"
        )
        assert l.is_active is True

    def test_register_lecturer_stores_department(self, user_service):
        l = user_service.register_lecturer(
            "l1", "Dr Nkosi", "nkosi@uni.ac.za", "pass", "Mathematics", "EMP001"
        )
        assert l.department == "Mathematics"

    def test_register_lecturer_duplicate_employee_number_raises_conflict(self, user_service):
        user_service.register_lecturer(
            "l1", "Dr Nkosi", "nkosi@uni.ac.za", "pass", "CS", "EMP001"
        )
        with pytest.raises(ConflictError, match="already registered"):
            user_service.register_lecturer(
                "l2", "Dr Smith", "smith@uni.ac.za", "pass", "Math", "EMP001"
            )

    def test_register_lecturer_empty_department_raises_validation(self, user_service):
        with pytest.raises(ValidationError, match="'department'"):
            user_service.register_lecturer(
                "l1", "Dr Nkosi", "nkosi@uni.ac.za", "pass", "", "EMP001"
            )


class TestLogin:

    def test_login_student_with_correct_credentials(self, user_service):
        user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass123", "STU001", 2
        )
        user = user_service.login("alice@uni.ac.za", "pass123", "STUDENT")
        assert user.email == "alice@uni.ac.za"

    def test_login_wrong_password_raises_validation(self, user_service):
        user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass123", "STU001", 2
        )
        with pytest.raises(ValidationError, match="Invalid email or password"):
            user_service.login("alice@uni.ac.za", "wrongpass", "STUDENT")

    def test_login_nonexistent_email_raises_not_found(self, user_service):
        with pytest.raises(NotFoundError):
            user_service.login("nobody@uni.ac.za", "pass", "STUDENT")

    def test_login_invalid_role_raises_validation(self, user_service):
        with pytest.raises(ValidationError, match="Invalid role"):
            user_service.login("alice@uni.ac.za", "pass", "ADMIN")

    def test_login_lecturer_with_correct_credentials(self, user_service):
        user_service.register_lecturer(
            "l1", "Dr Nkosi", "nkosi@uni.ac.za", "securepass", "CS", "EMP001"
        )
        user = user_service.login("nkosi@uni.ac.za", "securepass", "LECTURER")
        assert user.email == "nkosi@uni.ac.za"


class TestProfileManagement:

    def test_get_student_returns_correct_student(self, user_service):
        user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2
        )
        s = user_service.get_student("s1")
        assert s.name == "Alice"

    def test_get_student_not_found_raises_not_found(self, user_service):
        with pytest.raises(NotFoundError):
            user_service.get_student("s_missing")

    def test_update_profile_name(self, user_service):
        user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2
        )
        updated = user_service.update_profile("s1", "STUDENT", name="Alice Updated")
        assert updated.name == "Alice Updated"

    def test_update_profile_email_conflict_raises(self, user_service):
        user_service.register_student(
            "s1", "Alice", "alice@uni.ac.za", "pass", "STU001", 2
        )
        user_service.register_student(
            "s2", "Bob", "bob@uni.ac.za", "pass", "STU002", 1
        )
        with pytest.raises(ConflictError, match="already in use"):
            user_service.update_profile("s1", "STUDENT", email="bob@uni.ac.za")

    def test_get_all_students_returns_all(self, user_service):
        user_service.register_student("s1", "A", "a@u.ac.za", "p", "S1", 1)
        user_service.register_student("s2", "B", "b@u.ac.za", "p", "S2", 2)
        assert len(user_service.get_all_students()) == 2

    def test_get_all_lecturers_returns_all(self, user_service):
        user_service.register_lecturer("l1", "X", "x@u.ac.za", "p", "CS", "E1")
        user_service.register_lecturer("l2", "Y", "y@u.ac.za", "p", "Math", "E2")
        assert len(user_service.get_all_lecturers()) == 2