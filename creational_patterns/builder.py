"""
builder.py — Builder Pattern
Student Assignment Tracker

Pattern:  Builder
Use Case: Assignment construction — assignments have many optional fields
          (description, total marks, status, attachments). A builder lets
          lecturers configure each part step-by-step before the object is
          finalised, preventing telescoping constructors and invalid
          half-built objects.

Justification: The Assignment constructor already has 7 parameters. As
               features grow (rubric, attachment URLs, group flags), a
               builder is the clean solution. The director pre-wires common
               assignment templates (e.g. QuizDirector, EssayDirector).
"""

from datetime import date, timedelta
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Assignment Product (standalone, builder-native version)
# ---------------------------------------------------------------------------

class AssignmentProduct:
    """
    A fully-configured assignment built by AssignmentBuilder.
    Uses a plain __init__ so the builder controls all fields.
    """

    def __init__(self):
        self.assignment_id: str = ""
        self.title: str = ""
        self.description: str = ""
        self.due_date: date = date.today() + timedelta(days=7)
        self.total_marks: int = 100
        self.status: str = "DRAFT"
        self.allow_late: bool = False
        self.max_file_size_mb: int = 10
        self.instructions_url: str = ""
        self.rubric: dict = {}

    def __repr__(self) -> str:
        return (
            f"Assignment(id={self.assignment_id!r}, title={self.title!r}, "
            f"due={self.due_date}, marks={self.total_marks}, "
            f"late={self.allow_late}, status={self.status!r})"
        )


# ---------------------------------------------------------------------------
# Abstract Builder
# ---------------------------------------------------------------------------

class AssignmentBuilder(ABC):
    """Declares all steps for building an AssignmentProduct."""

    @abstractmethod
    def set_id(self, assignment_id: str) -> "AssignmentBuilder": pass

    @abstractmethod
    def set_title(self, title: str) -> "AssignmentBuilder": pass

    @abstractmethod
    def set_description(self, description: str) -> "AssignmentBuilder": pass

    @abstractmethod
    def set_due_date(self, due_date: date) -> "AssignmentBuilder": pass

    @abstractmethod
    def set_total_marks(self, marks: int) -> "AssignmentBuilder": pass

    @abstractmethod
    def set_allow_late(self, allow: bool) -> "AssignmentBuilder": pass

    @abstractmethod
    def set_max_file_size(self, size_mb: int) -> "AssignmentBuilder": pass

    @abstractmethod
    def set_instructions_url(self, url: str) -> "AssignmentBuilder": pass

    @abstractmethod
    def set_rubric(self, rubric: dict) -> "AssignmentBuilder": pass

    @abstractmethod
    def build(self) -> AssignmentProduct: pass


# ---------------------------------------------------------------------------
# Concrete Builder
# ---------------------------------------------------------------------------

class ConcreteAssignmentBuilder(AssignmentBuilder):
    """
    Builds an AssignmentProduct step by step.
    Each method returns self to support method chaining.
    """

    def __init__(self):
        self._reset()

    def _reset(self):
        self._assignment = AssignmentProduct()

    def set_id(self, assignment_id: str) -> "ConcreteAssignmentBuilder":
        self._assignment.assignment_id = assignment_id
        return self

    def set_title(self, title: str) -> "ConcreteAssignmentBuilder":
        if not title.strip():
            raise ValueError("Assignment title cannot be empty.")
        self._assignment.title = title
        return self

    def set_description(self, description: str) -> "ConcreteAssignmentBuilder":
        self._assignment.description = description
        return self

    def set_due_date(self, due_date: date) -> "ConcreteAssignmentBuilder":
        if due_date < date.today():
            raise ValueError("Due date cannot be in the past.")
        self._assignment.due_date = due_date
        return self

    def set_total_marks(self, marks: int) -> "ConcreteAssignmentBuilder":
        if marks <= 0:
            raise ValueError("Total marks must be a positive integer.")
        self._assignment.total_marks = marks
        return self

    def set_allow_late(self, allow: bool) -> "ConcreteAssignmentBuilder":
        self._assignment.allow_late = allow
        return self

    def set_max_file_size(self, size_mb: int) -> "ConcreteAssignmentBuilder":
        if size_mb <= 0:
            raise ValueError("File size limit must be positive.")
        self._assignment.max_file_size_mb = size_mb
        return self

    def set_instructions_url(self, url: str) -> "ConcreteAssignmentBuilder":
        self._assignment.instructions_url = url
        return self

    def set_rubric(self, rubric: dict) -> "ConcreteAssignmentBuilder":
        self._assignment.rubric = rubric
        return self

    def build(self) -> AssignmentProduct:
        """Finalise and return the product. Resets the builder for reuse."""
        if not self._assignment.title:
            raise ValueError("Cannot build assignment without a title.")
        if not self._assignment.assignment_id:
            raise ValueError("Cannot build assignment without an ID.")
        result = self._assignment
        self._reset()
        return result


# ---------------------------------------------------------------------------
# Director — pre-wires common assignment templates
# ---------------------------------------------------------------------------

class AssignmentDirector:
    """
    Director knows how to use a builder to construct common assignment types.
    Clients use the director for standard templates or the builder directly
    for fully custom assignments.
    """

    def __init__(self, builder: AssignmentBuilder):
        self._builder = builder

    def build_quiz(self, assignment_id: str, title: str) -> AssignmentProduct:
        """Short quiz: 30 marks, 2-day deadline, no late submissions, small files."""
        return (
            self._builder
            .set_id(assignment_id)
            .set_title(title)
            .set_description("Online quiz — complete within the time window.")
            .set_due_date(date.today() + timedelta(days=2))
            .set_total_marks(30)
            .set_allow_late(False)
            .set_max_file_size(2)
            .build()
        )

    def build_essay(self, assignment_id: str, title: str) -> AssignmentProduct:
        """Long-form essay: 100 marks, 14-day deadline, late allowed, larger files."""
        return (
            self._builder
            .set_id(assignment_id)
            .set_title(title)
            .set_description("Written essay — submit as PDF.")
            .set_due_date(date.today() + timedelta(days=14))
            .set_total_marks(100)
            .set_allow_late(True)
            .set_max_file_size(20)
            .set_rubric({"structure": 20, "content": 50, "references": 30})
            .build()
        )

    def build_project(self, assignment_id: str, title: str) -> AssignmentProduct:
        """Group project: 150 marks, 30-day deadline, GitHub link required."""
        return (
            self._builder
            .set_id(assignment_id)
            .set_title(title)
            .set_description("Group project — submit GitHub repo link.")
            .set_due_date(date.today() + timedelta(days=30))
            .set_total_marks(150)
            .set_allow_late(False)
            .set_max_file_size(50)
            .set_rubric({"design": 40, "implementation": 70, "testing": 40})
            .build()
        )


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    builder = ConcreteAssignmentBuilder()
    director = AssignmentDirector(builder)

    quiz = director.build_quiz("a001", "Week 3 Quiz")
    print(f"Quiz:    {quiz}")

    essay = director.build_essay("a002", "Software Ethics Essay")
    print(f"Essay:   {essay}")

    project = director.build_project("a003", "Assignment Tracker Project")
    print(f"Project: {project}")

    # Direct builder usage for a custom assignment
    custom = (
        ConcreteAssignmentBuilder()
        .set_id("a004")
        .set_title("Custom Research Assignment")
        .set_description("Research a topic of your choice.")
        .set_due_date(date.today() + timedelta(days=10))
        .set_total_marks(75)
        .set_allow_late(True)
        .set_instructions_url("https://uni.ac.za/research-guide")
        .build()
    )
    print(f"Custom:  {custom}")