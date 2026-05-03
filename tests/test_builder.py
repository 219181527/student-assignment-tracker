"""
tests/test_builder.py
Tests for the Builder pattern — ConcreteAssignmentBuilder and AssignmentDirector
"""

import pytest
from datetime import date, timedelta
from creational_patterns.builder import (
    ConcreteAssignmentBuilder,
    AssignmentDirector,
    AssignmentProduct,
)


@pytest.fixture
def builder():
    return ConcreteAssignmentBuilder()


@pytest.fixture
def director(builder):
    return AssignmentDirector(builder)


class TestConcreteAssignmentBuilder:

    def test_builds_valid_assignment(self, builder):
        result = (
            builder
            .set_id("a001")
            .set_title("Test Assignment")
            .set_due_date(date.today() + timedelta(days=7))
            .set_total_marks(100)
            .build()
        )
        assert isinstance(result, AssignmentProduct)

    def test_title_is_set_correctly(self, builder):
        result = (
            builder.set_id("a1").set_title("My Title")
            .set_due_date(date.today() + timedelta(days=1))
            .set_total_marks(50).build()
        )
        assert result.title == "My Title"

    def test_due_date_is_set_correctly(self, builder):
        target = date.today() + timedelta(days=10)
        result = (
            builder.set_id("a2").set_title("T")
            .set_due_date(target).set_total_marks(50).build()
        )
        assert result.due_date == target

    def test_total_marks_is_set(self, builder):
        result = (
            builder.set_id("a3").set_title("T")
            .set_due_date(date.today() + timedelta(days=1))
            .set_total_marks(75).build()
        )
        assert result.total_marks == 75

    def test_allow_late_defaults_to_false(self, builder):
        result = (
            builder.set_id("a4").set_title("T")
            .set_due_date(date.today() + timedelta(days=1))
            .set_total_marks(50).build()
        )
        assert result.allow_late is False

    def test_allow_late_can_be_set_true(self, builder):
        result = (
            builder.set_id("a5").set_title("T")
            .set_due_date(date.today() + timedelta(days=1))
            .set_total_marks(50).set_allow_late(True).build()
        )
        assert result.allow_late is True

    def test_rubric_stored_as_dict(self, builder):
        rubric = {"design": 40, "code": 60}
        result = (
            builder.set_id("a6").set_title("T")
            .set_due_date(date.today() + timedelta(days=1))
            .set_total_marks(100).set_rubric(rubric).build()
        )
        assert result.rubric == rubric

    def test_instructions_url_stored(self, builder):
        url = "https://uni.ac.za/guide"
        result = (
            builder.set_id("a7").set_title("T")
            .set_due_date(date.today() + timedelta(days=1))
            .set_total_marks(50).set_instructions_url(url).build()
        )
        assert result.instructions_url == url

    def test_builder_resets_after_build(self, builder):
        builder.set_id("a8").set_title("First").set_due_date(
            date.today() + timedelta(days=1)).set_total_marks(50).build()
        # After build, builder should be reset — building without fields should fail
        with pytest.raises(ValueError):
            builder.build()

    def test_method_chaining_returns_builder(self, builder):
        result = builder.set_id("a9")
        assert result is builder

    def test_max_file_size_stored(self, builder):
        result = (
            builder.set_id("a10").set_title("T")
            .set_due_date(date.today() + timedelta(days=1))
            .set_total_marks(50).set_max_file_size(25).build()
        )
        assert result.max_file_size_mb == 25


class TestBuilderEdgeCases:

    def test_empty_title_raises_value_error(self, builder):
        with pytest.raises(ValueError, match="empty"):
            builder.set_id("a11").set_title("")

    def test_past_due_date_raises_value_error(self, builder):
        with pytest.raises(ValueError, match="past"):
            builder.set_id("a12").set_title("T").set_due_date(
                date.today() - timedelta(days=1))

    def test_zero_marks_raises_value_error(self, builder):
        with pytest.raises(ValueError, match="positive"):
            builder.set_id("a13").set_title("T").set_total_marks(0)

    def test_negative_marks_raises_value_error(self, builder):
        with pytest.raises(ValueError, match="positive"):
            builder.set_id("a14").set_title("T").set_total_marks(-10)

    def test_zero_file_size_raises_value_error(self, builder):
        with pytest.raises(ValueError, match="positive"):
            builder.set_id("a15").set_title("T").set_max_file_size(0)

    def test_build_without_id_raises_value_error(self, builder):
        with pytest.raises(ValueError, match="ID"):
            builder.set_title("T").set_due_date(
                date.today() + timedelta(days=1)).set_total_marks(50).build()

    def test_build_without_title_raises_value_error(self, builder):
        with pytest.raises(ValueError, match="title"):
            builder.set_id("a16").set_due_date(
                date.today() + timedelta(days=1)).set_total_marks(50).build()


class TestAssignmentDirector:

    def test_quiz_total_marks_is_30(self, director):
        quiz = director.build_quiz("q1", "Week 1 Quiz")
        assert quiz.total_marks == 30

    def test_quiz_does_not_allow_late(self, director):
        quiz = director.build_quiz("q2", "Quiz")
        assert quiz.allow_late is False

    def test_quiz_due_in_2_days(self, director):
        quiz = director.build_quiz("q3", "Quiz")
        assert quiz.due_date == date.today() + timedelta(days=2)

    def test_essay_total_marks_is_100(self, director):
        essay = director.build_essay("e1", "Essay")
        assert essay.total_marks == 100

    def test_essay_allows_late(self, director):
        essay = director.build_essay("e2", "Essay")
        assert essay.allow_late is True

    def test_essay_due_in_14_days(self, director):
        essay = director.build_essay("e3", "Essay")
        assert essay.due_date == date.today() + timedelta(days=14)

    def test_essay_has_rubric(self, director):
        essay = director.build_essay("e4", "Essay")
        assert isinstance(essay.rubric, dict)
        assert len(essay.rubric) > 0

    def test_project_total_marks_is_150(self, director):
        project = director.build_project("p1", "Project")
        assert project.total_marks == 150

    def test_project_due_in_30_days(self, director):
        project = director.build_project("p2", "Project")
        assert project.due_date == date.today() + timedelta(days=30)

    def test_director_can_build_multiple_sequentially(self, director):
        q = director.build_quiz("q10", "Q")
        e = director.build_essay("e10", "E")
        p = director.build_project("p10", "P")
        assert q.total_marks == 30
        assert e.total_marks == 100
        assert p.total_marks == 150