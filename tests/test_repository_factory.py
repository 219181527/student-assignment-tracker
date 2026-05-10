"""
tests/test_repository_factory.py — Tests for RepositoryFactory
Student Assignment Tracker — Assignment 11, Task 3
"""

import sys
sys.path.insert(0, '.')

import pytest
from repositories.factory import RepositoryFactory
from repositories.inmemory.implementations import (
    InMemoryStudentRepository,
    InMemoryLecturerRepository,
    InMemoryCourseRepository,
    InMemoryAssignmentRepository,
    InMemorySubmissionRepository,
    InMemoryGradeRepository,
    InMemoryNotificationRepository,
    InMemoryEnrollmentRepository,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def memory_factory():
    return RepositoryFactory(storage_type="MEMORY")


# ---------------------------------------------------------------------------
# Instantiation tests
# ---------------------------------------------------------------------------

class TestRepositoryFactoryInstantiation:

    def test_default_storage_type_is_memory(self):
        factory = RepositoryFactory()
        assert factory.storage_type == "MEMORY"

    def test_explicit_memory_storage_type(self, memory_factory):
        assert memory_factory.storage_type == "MEMORY"

    def test_storage_type_case_insensitive_lower(self):
        factory = RepositoryFactory(storage_type="memory")
        assert factory.storage_type == "MEMORY"

    def test_storage_type_case_insensitive_mixed(self):
        factory = RepositoryFactory(storage_type="Memory")
        assert factory.storage_type == "MEMORY"

    def test_unknown_storage_type_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown storage type"):
            RepositoryFactory(storage_type="REDIS")

    def test_empty_storage_type_raises_value_error(self):
        with pytest.raises(ValueError):
            RepositoryFactory(storage_type="")

    def test_repr_contains_storage_type(self, memory_factory):
        assert "MEMORY" in repr(memory_factory)


# ---------------------------------------------------------------------------
# Correct implementation type returned per entity
# ---------------------------------------------------------------------------

class TestMemoryRepositoryTypes:

    def test_get_student_repository_returns_inmemory(self, memory_factory):
        assert isinstance(memory_factory.get_student_repository(),
                          InMemoryStudentRepository)

    def test_get_lecturer_repository_returns_inmemory(self, memory_factory):
        assert isinstance(memory_factory.get_lecturer_repository(),
                          InMemoryLecturerRepository)

    def test_get_course_repository_returns_inmemory(self, memory_factory):
        assert isinstance(memory_factory.get_course_repository(),
                          InMemoryCourseRepository)

    def test_get_assignment_repository_returns_inmemory(self, memory_factory):
        assert isinstance(memory_factory.get_assignment_repository(),
                          InMemoryAssignmentRepository)

    def test_get_submission_repository_returns_inmemory(self, memory_factory):
        assert isinstance(memory_factory.get_submission_repository(),
                          InMemorySubmissionRepository)

    def test_get_grade_repository_returns_inmemory(self, memory_factory):
        assert isinstance(memory_factory.get_grade_repository(),
                          InMemoryGradeRepository)

    def test_get_notification_repository_returns_inmemory(self, memory_factory):
        assert isinstance(memory_factory.get_notification_repository(),
                          InMemoryNotificationRepository)

    def test_get_enrollment_repository_returns_inmemory(self, memory_factory):
        assert isinstance(memory_factory.get_enrollment_repository(),
                          InMemoryEnrollmentRepository)


# ---------------------------------------------------------------------------
# Singleton-per-type: same instance returned on repeated calls
# ---------------------------------------------------------------------------

class TestRepositoryInstanceCaching:

    def test_student_repo_same_instance_on_repeated_calls(self, memory_factory):
        r1 = memory_factory.get_student_repository()
        r2 = memory_factory.get_student_repository()
        assert r1 is r2

    def test_lecturer_repo_same_instance(self, memory_factory):
        assert (memory_factory.get_lecturer_repository() is
                memory_factory.get_lecturer_repository())

    def test_course_repo_same_instance(self, memory_factory):
        assert (memory_factory.get_course_repository() is
                memory_factory.get_course_repository())

    def test_assignment_repo_same_instance(self, memory_factory):
        assert (memory_factory.get_assignment_repository() is
                memory_factory.get_assignment_repository())

    def test_submission_repo_same_instance(self, memory_factory):
        assert (memory_factory.get_submission_repository() is
                memory_factory.get_submission_repository())

    def test_grade_repo_same_instance(self, memory_factory):
        assert (memory_factory.get_grade_repository() is
                memory_factory.get_grade_repository())

    def test_two_factories_return_different_instances(self):
        """Two separate factories must not share state."""
        f1 = RepositoryFactory("MEMORY")
        f2 = RepositoryFactory("MEMORY")
        assert f1.get_student_repository() is not f2.get_student_repository()

    def test_state_persists_within_same_factory(self, memory_factory):
        """Data saved via one call is visible via another call to the same factory."""
        from src.student import Student
        student = Student("s_fac", "Factory Test", "f@uni.ac.za",
                          "pass", "STU_FAC", 1)
        student.register()
        repo1 = memory_factory.get_student_repository()
        repo1.save(student)
        repo2 = memory_factory.get_student_repository()  # Same instance
        assert repo2.find_by_id("s_fac") is not None


# ---------------------------------------------------------------------------
# DATABASE storage type raises NotImplementedError
# ---------------------------------------------------------------------------

class TestDatabaseStorageNotImplemented:

    def test_database_student_repo_raises(self):
        factory = RepositoryFactory("DATABASE")
        with pytest.raises(NotImplementedError):
            factory.get_student_repository()

    def test_database_lecturer_repo_raises(self):
        factory = RepositoryFactory("DATABASE")
        with pytest.raises(NotImplementedError):
            factory.get_lecturer_repository()

    def test_database_course_repo_raises(self):
        factory = RepositoryFactory("DATABASE")
        with pytest.raises(NotImplementedError):
            factory.get_course_repository()

    def test_database_assignment_repo_raises(self):
        factory = RepositoryFactory("DATABASE")
        with pytest.raises(NotImplementedError):
            factory.get_assignment_repository()

    def test_database_submission_repo_raises(self):
        factory = RepositoryFactory("DATABASE")
        with pytest.raises(NotImplementedError):
            factory.get_submission_repository()

    def test_database_grade_repo_raises(self):
        factory = RepositoryFactory("DATABASE")
        with pytest.raises(NotImplementedError):
            factory.get_grade_repository()

    def test_database_enrollment_repo_raises(self):
        factory = RepositoryFactory("DATABASE")
        with pytest.raises(NotImplementedError):
            factory.get_enrollment_repository()


# ---------------------------------------------------------------------------
# Swap storage backends — same interface, different implementation
# ---------------------------------------------------------------------------

class TestStorageSwapping:

    def test_memory_and_database_factories_return_same_interface(self):
        """
        Both factories' student repos must satisfy the StudentRepository
        interface — callers are decoupled from the concrete type.
        """
        from repositories.interfaces import StudentRepository
        memory_repo = RepositoryFactory("MEMORY").get_student_repository()
        assert isinstance(memory_repo, StudentRepository)

    def test_switching_factory_does_not_affect_other_factory_state(self):
        """Data in a MEMORY factory is invisible to a second MEMORY factory."""
        from src.student import Student
        f1 = RepositoryFactory("MEMORY")
        f2 = RepositoryFactory("MEMORY")
        s = Student("s_iso", "Isolated", "iso@uni.ac.za", "p", "STU_ISO", 1)
        s.register()
        f1.get_student_repository().save(s)
        assert f2.get_student_repository().find_by_id("s_iso") is None