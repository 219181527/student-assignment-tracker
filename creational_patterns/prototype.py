"""
prototype.py — Prototype Pattern
Student Assignment Tracker

Pattern:  Prototype
Use Case: Submission templates — when a lecturer creates a recurring
          assignment (e.g. weekly lab reports), a pre-configured
          Submission prototype can be cloned for each student rather than
          constructing a fresh object with repeated defaults every time.
          Also used to clone AssignmentProduct objects from the Builder
          as templates for the next semester.

Justification: Cloning is cheaper than re-running full construction logic
               when the base configuration is identical across many objects.
               The prototype registry caches named templates for reuse.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import copy
from datetime import date, timedelta
from typing import Dict


# ---------------------------------------------------------------------------
# Prototype interface (mixin)
# ---------------------------------------------------------------------------

class Prototype:
    """Mixin that adds shallow and deep clone methods to any class."""

    def clone(self):
        """Shallow clone — shared references for immutable fields."""
        return copy.copy(self)

    def deep_clone(self):
        """Deep clone — fully independent copy, no shared state."""
        return copy.deepcopy(self)


# ---------------------------------------------------------------------------
# Prototype-capable Assignment Template
# ---------------------------------------------------------------------------

class AssignmentTemplate(Prototype):
    """
    A cloneable assignment template. Stores a pre-configured assignment
    structure that can be cloned and customised for a new semester or
    a different course without rebuilding from scratch.
    """

    def __init__(self, template_id: str, title: str, description: str,
                 total_marks: int, duration_days: int,
                 allow_late: bool = False, rubric: dict = None):
        self.template_id = template_id
        self.title = title
        self.description = description
        self.total_marks = total_marks
        self.duration_days = duration_days  # Deadline = today + duration_days
        self.allow_late = allow_late
        self.rubric = rubric or {}

    def to_assignment_dict(self, course_code: str, semester: str) -> dict:
        """Render this template as a dict ready to pass to AssignmentBuilder."""
        return {
            "assignment_id": f"{course_code}_{self.template_id}_{semester}",
            "title": f"{self.title} ({semester})",
            "description": self.description,
            "due_date": date.today() + timedelta(days=self.duration_days),
            "total_marks": self.total_marks,
            "allow_late": self.allow_late,
            "rubric": self.rubric,
        }

    def __repr__(self) -> str:
        return (f"AssignmentTemplate(id={self.template_id!r}, "
                f"title={self.title!r}, marks={self.total_marks})")


# ---------------------------------------------------------------------------
# Prototype Registry
# ---------------------------------------------------------------------------

class AssignmentTemplateRegistry:
    """
    Stores named AssignmentTemplate prototypes.
    Clients call get() to retrieve a deep clone — the original is never mutated.
    """

    def __init__(self):
        self._templates: Dict[str, AssignmentTemplate] = {}

    def register(self, name: str, template: AssignmentTemplate) -> None:
        """Register a template under a name key."""
        self._templates[name] = template

    def get(self, name: str) -> AssignmentTemplate:
        """
        Return a deep clone of the named template.
        Raises KeyError if the template is not registered.
        """
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not found in registry.")
        return self._templates[name].deep_clone()

    def list_templates(self) -> list:
        return list(self._templates.keys())


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    registry = AssignmentTemplateRegistry()

    # Register reusable base templates
    registry.register("weekly_lab", AssignmentTemplate(
        template_id="lab",
        title="Weekly Lab Report",
        description="Submit your lab report as a PDF.",
        total_marks=20,
        duration_days=7,
        allow_late=False,
        rubric={"methodology": 8, "results": 7, "conclusion": 5},
    ))

    registry.register("domain_model", AssignmentTemplate(
        template_id="dm",
        title="Domain Model",
        description="Design a domain model for the given scenario.",
        total_marks=100,
        duration_days=14,
        allow_late=True,
        rubric={"entities": 30, "relationships": 40, "documentation": 30},
    ))

    # Clone templates for Semester 1, 2026
    lab_s1 = registry.get("weekly_lab")
    lab_s2 = registry.get("weekly_lab")

    # Customise clone without touching the original
    lab_s1.title = "Week 1 Lab Report"
    lab_s2.title = "Week 2 Lab Report"
    lab_s2.duration_days = 14  # Extended for week 2

    print(f"Original: {registry._templates['weekly_lab']}")
    print(f"Clone 1:  {lab_s1}")
    print(f"Clone 2:  {lab_s2}")

    dm = registry.get("domain_model")
    print(f"\nDomain Model template dict:")
    for k, v in dm.to_assignment_dict("CS301", "S1-2026").items():
        print(f"  {k}: {v}")

    print(f"\nRegistered templates: {registry.list_templates()}")