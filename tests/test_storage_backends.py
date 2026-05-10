"""
tests/test_storage_backends.py — Tests for FileSystem and Database Stubs
Student Assignment Tracker — Assignment 11, Task 4
"""

import sys, os, tempfile, json
sys.path.insert(0, '.')

import pytest
from repositories.filesystem.implementations import (
    FileSystemStudentRepository,
    FileSystemLecturerRepository,
    FileSystemCourseRepository,
    FileSystemNotificationRepository,
)
from repositories.database.stubs import (
    DatabaseStudentRepository,
    DatabaseLecturerRepository,
    DatabaseCourseRepository,
    DatabaseAssignmentRepository,
    DatabaseSubmissionRepository,
    DatabaseGradeRepository,
    DatabaseEnrollmentRepository,
)
from repositories.factory import RepositoryFactory
from src.student import Student
from src.lecturer import Lecturer
from src.course import Course
from src.notification import Notification


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_student(uid="s1", num="STU001"):
    s = Student(uid, "Alice", f"{uid}@uni.ac.za", "pass", num, 2)
    s.register()
    return s

def make_lecturer(uid="l1"):
    l = Lecturer(uid, "Dr Nkosi", f"{uid}@uni.ac.za", "pass", "CS", f"EMP{uid}")
    l.register()
    return l

def make_course(cid="c1", code="CS301"):
    return Course(cid, "Software Engineering", code, 15)


# ---------------------------------------------------------------------------
# FileSystem — Student Repository
# ---------------------------------------------------------------------------

class TestFileSystemStudentRepository:

    @pytest.fixture
    def repo(self, tmp_path):
        """Use pytest's tmp_path for a clean JSON file per test."""
        return FileSystemStudentRepository(str(tmp_path / "students.json"))

    def test_save_creates_json_file(self, repo, tmp_path):
        repo.save(make_student())
        assert os.path.exists(str(tmp_path / "students.json"))

    def test_save_and_find_by_id(self, repo):
        s = make_student()
        repo.save(s)
        result = repo.find_by_id("s1")
        assert result is not None
        assert result.name == "Alice"

    def test_find_by_id_missing_returns_none(self, repo):
        assert repo.find_by_id("missing") is None

    def test_save_overwrites_existing(self, repo):
        s = make_student()
        repo.save(s)
        s.update_profile(name="Alice Updated")
        repo.save(s)
        assert repo.count() == 1
        assert repo.find_by_id("s1").name == "Alice Updated"

    def test_find_all_returns_all(self, repo):
        repo.save(make_student("s1", "STU001"))
        repo.save(make_student("s2", "STU002"))
        assert len(repo.find_all()) == 2

    def test_delete_removes_entry(self, repo):
        repo.save(make_student())
        repo.delete("s1")
        assert repo.find_by_id("s1") is None

    def test_delete_missing_raises_key_error(self, repo):
        with pytest.raises(KeyError):
            repo.delete("missing")

    def test_exists_true(self, repo):
        repo.save(make_student())
        assert repo.exists("s1") is True

    def test_exists_false(self, repo):
        assert repo.exists("nobody") is False

    def test_count(self, repo):
        repo.save(make_student("s1", "STU001"))
        repo.save(make_student("s2", "STU002"))
        assert repo.count() == 2

    def test_persists_to_json_correctly(self, repo, tmp_path):
        repo.save(make_student())
        with open(str(tmp_path / "students.json")) as f:
            data = json.load(f)
        assert "s1" in data
        assert data["s1"]["name"] == "Alice"
        assert data["s1"]["student_number"] == "STU001"

    def test_find_by_student_number(self, repo):
        repo.save(make_student("s1", "219181527"))
        result = repo.find_by_student_number("219181527")
        assert result is not None
        assert result.user_id == "s1"

    def test_find_by_student_number_missing_returns_none(self, repo):
        assert repo.find_by_student_number("MISSING") is None

    def test_data_survives_reload(self, tmp_path):
        """Data written by one instance is readable by a second instance."""
        path = str(tmp_path / "students.json")
        repo1 = FileSystemStudentRepository(path)
        repo1.save(make_student())
        repo2 = FileSystemStudentRepository(path)
        assert repo2.find_by_id("s1").name == "Alice"


# ---------------------------------------------------------------------------
# FileSystem — Course Repository
# ---------------------------------------------------------------------------

class TestFileSystemCourseRepository:

    @pytest.fixture
    def repo(self, tmp_path):
        return FileSystemCourseRepository(str(tmp_path / "courses.json"))

    def test_save_and_find_by_id(self, repo):
        repo.save(make_course())
        result = repo.find_by_id("c1")
        assert result.course_code == "CS301"

    def test_find_by_code(self, repo):
        repo.save(make_course("c1", "CS301"))
        result = repo.find_by_code("CS301")
        assert result is not None
        assert result.course_id == "c1"

    def test_find_active(self, repo):
        repo.save(make_course("c1", "CS301"))
        assert len(repo.find_active()) == 1

    def test_find_active_after_deactivate(self, repo):
        c = make_course()
        c.deactivate()
        repo.save(c)
        assert repo.find_active() == []

    def test_delete_and_count(self, repo):
        repo.save(make_course("c1", "CS301"))
        repo.save(make_course("c2", "CS302"))
        repo.delete("c1")
        assert repo.count() == 1


# ---------------------------------------------------------------------------
# FileSystem — Notification Repository (full deserialize supported)
# ---------------------------------------------------------------------------

class TestFileSystemNotificationRepository:

    @pytest.fixture
    def repo(self, tmp_path):
        return FileSystemNotificationRepository(str(tmp_path / "notifications.json"))

    def test_save_and_find_by_id(self, repo):
        n = Notification("n1", "Test alert", "DEADLINE", source=None)
        repo.save(n)
        result = repo.find_by_id("n1")
        assert result is not None
        assert result.trigger_type == "DEADLINE"

    def test_find_by_trigger_type(self, repo):
        n1 = Notification("n1", "Deadline!", "DEADLINE", source=None)
        n2 = Notification("n2", "Graded!", "GRADE", source=None)
        repo.save(n1)
        repo.save(n2)
        results = repo.find_by_trigger_type("DEADLINE")
        assert len(results) == 1
        assert results[0].notification_id == "n1"

    def test_mark_as_read_persisted(self, repo, tmp_path):
        n = Notification("n1", "Alert", "SUBMISSION", source=None)
        n.mark_as_read()
        repo.save(n)
        result = repo.find_by_id("n1")
        assert result.get_status() == "READ"

    def test_find_by_student(self, repo):
        n = Notification("n1", "Hello", "GRADE", source=None)
        repo.save(n, student_id="s1")
        results = repo.find_by_student("s1")
        assert len(results) == 1

    def test_find_unread_by_student(self, repo):
        n1 = Notification("n1", "Unread", "DEADLINE", source=None)
        n2 = Notification("n2", "Read", "GRADE", source=None)
        n2.mark_as_read()
        repo.save(n1, student_id="s1")
        repo.save(n2, student_id="s1")
        unread = repo.find_unread_by_student("s1")
        assert len(unread) == 1
        assert unread[0].notification_id == "n1"


# ---------------------------------------------------------------------------
# Database Stubs — all methods raise NotImplementedError
# ---------------------------------------------------------------------------

class TestDatabaseStubs:

    def test_student_save_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseStudentRepository().save(make_student())

    def test_student_find_by_id_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseStudentRepository().find_by_id("s1")

    def test_student_find_all_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseStudentRepository().find_all()

    def test_student_delete_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseStudentRepository().delete("s1")

    def test_student_exists_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseStudentRepository().exists("s1")

    def test_student_count_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseStudentRepository().count()

    def test_student_find_by_student_number_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseStudentRepository().find_by_student_number("STU001")

    def test_lecturer_save_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseLecturerRepository().save(make_lecturer())

    def test_course_save_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseCourseRepository().save(make_course())

    def test_assignment_find_overdue_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseAssignmentRepository().find_overdue()

    def test_submission_find_by_status_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseSubmissionRepository().find_by_status("GRADED")

    def test_grade_find_by_submission_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseGradeRepository().find_by_submission("sub1")

    def test_enrollment_find_by_status_raises(self):
        with pytest.raises(NotImplementedError):
            DatabaseEnrollmentRepository().find_by_status("ACTIVE")


# ---------------------------------------------------------------------------
# Factory — FILESYSTEM storage type routing
# ---------------------------------------------------------------------------

class TestFilesystemFactory:

    def test_filesystem_factory_student_repo_type(self, tmp_path, monkeypatch):
        """
        RepositoryFactory("FILESYSTEM") must return a FileSystem repo.
        We monkeypatch the data path to use tmp_path.
        """
        from repositories.filesystem.implementations import FileSystemStudentRepository

        original_make = RepositoryFactory._make_student_repo

        def patched_make(self_inner):
            return FileSystemStudentRepository(str(tmp_path / "students.json"))

        monkeypatch.setattr(RepositoryFactory, "_make_student_repo", patched_make)
        factory = RepositoryFactory("FILESYSTEM")
        repo = factory.get_student_repository()
        assert isinstance(repo, FileSystemStudentRepository)

    def test_filesystem_factory_crud_round_trip(self, tmp_path, monkeypatch):
        """Data saved via FILESYSTEM factory survives a save/find cycle."""
        from repositories.filesystem.implementations import FileSystemStudentRepository

        def patched_make(self_inner):
            return FileSystemStudentRepository(str(tmp_path / "students.json"))

        monkeypatch.setattr(RepositoryFactory, "_make_student_repo", patched_make)
        factory = RepositoryFactory("FILESYSTEM")
        s = make_student("s_fs", "STU_FS")
        factory.get_student_repository().save(s)
        result = factory.get_student_repository().find_by_id("s_fs")
        assert result.name == "Alice"