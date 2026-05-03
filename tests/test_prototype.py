"""
tests/test_prototype.py
Tests for the Prototype pattern — AssignmentTemplate and AssignmentTemplateRegistry
"""

import pytest
from creational_patterns.prototype import AssignmentTemplate, AssignmentTemplateRegistry


@pytest.fixture
def lab_template():
    return AssignmentTemplate(
        template_id="lab",
        title="Weekly Lab Report",
        description="Submit your lab report as PDF.",
        total_marks=20,
        duration_days=7,
        allow_late=False,
        rubric={"methodology": 8, "results": 7, "conclusion": 5},
    )


@pytest.fixture
def registry(lab_template):
    reg = AssignmentTemplateRegistry()
    reg.register("weekly_lab", lab_template)
    reg.register("domain_model", AssignmentTemplate(
        "dm", "Domain Model", "Design a domain model.", 100, 14, True,
        {"entities": 30, "relationships": 40, "docs": 30},
    ))
    return reg


class TestAssignmentTemplateClone:

    def test_clone_is_not_same_object(self, lab_template):
        clone = lab_template.clone()
        assert clone is not lab_template

    def test_deep_clone_is_not_same_object(self, lab_template):
        clone = lab_template.deep_clone()
        assert clone is not lab_template

    def test_clone_has_same_title(self, lab_template):
        clone = lab_template.clone()
        assert clone.title == lab_template.title

    def test_clone_has_same_total_marks(self, lab_template):
        clone = lab_template.clone()
        assert clone.total_marks == lab_template.total_marks

    def test_deep_clone_rubric_is_independent(self, lab_template):
        """Mutating deep clone's rubric must not affect the original."""
        clone = lab_template.deep_clone()
        clone.rubric["new_key"] = 99
        assert "new_key" not in lab_template.rubric

    def test_shallow_clone_rubric_is_shared(self, lab_template):
        """Shallow clone shares mutable rubric dict with original."""
        clone = lab_template.clone()
        clone.rubric["new_key"] = 99
        # Shallow copy — original rubric IS affected (expected behaviour)
        assert "new_key" in lab_template.rubric

    def test_mutating_clone_title_does_not_affect_original(self, lab_template):
        clone = lab_template.deep_clone()
        clone.title = "Modified Title"
        assert lab_template.title == "Weekly Lab Report"

    def test_clone_preserves_duration_days(self, lab_template):
        clone = lab_template.deep_clone()
        assert clone.duration_days == lab_template.duration_days

    def test_clone_preserves_allow_late(self, lab_template):
        clone = lab_template.deep_clone()
        assert clone.allow_late == lab_template.allow_late


class TestAssignmentTemplateRegistry:

    def test_registered_template_retrievable(self, registry):
        template = registry.get("weekly_lab")
        assert template is not None

    def test_get_returns_deep_clone_not_original(self, registry):
        original = registry._templates["weekly_lab"]
        clone = registry.get("weekly_lab")
        assert clone is not original

    def test_two_gets_return_independent_objects(self, registry):
        t1 = registry.get("weekly_lab")
        t2 = registry.get("weekly_lab")
        assert t1 is not t2

    def test_mutating_clone_does_not_affect_registry(self, registry):
        clone = registry.get("weekly_lab")
        clone.title = "Changed"
        original = registry._templates["weekly_lab"]
        assert original.title == "Weekly Lab Report"

    def test_unknown_key_raises_key_error(self, registry):
        with pytest.raises(KeyError, match="not found"):
            registry.get("nonexistent_template")

    def test_list_templates_returns_all_keys(self, registry):
        keys = registry.list_templates()
        assert "weekly_lab" in keys
        assert "domain_model" in keys

    def test_list_templates_count(self, registry):
        assert len(registry.list_templates()) == 2

    def test_to_assignment_dict_has_required_keys(self, registry):
        template = registry.get("weekly_lab")
        d = template.to_assignment_dict("CS301", "S1-2026")
        for key in ("assignment_id", "title", "description", "due_date", "total_marks"):
            assert key in d

    def test_to_assignment_dict_id_contains_course_code(self, registry):
        template = registry.get("weekly_lab")
        d = template.to_assignment_dict("CS301", "S1-2026")
        assert "CS301" in d["assignment_id"]

    def test_to_assignment_dict_title_contains_semester(self, registry):
        template = registry.get("weekly_lab")
        d = template.to_assignment_dict("CS301", "S1-2026")
        assert "S1-2026" in d["title"]

    def test_register_overwrites_existing_key(self, registry, lab_template):
        new_template = AssignmentTemplate("lab2", "New Lab", "New desc.", 30, 5)
        registry.register("weekly_lab", new_template)
        retrieved = registry.get("weekly_lab")
        assert retrieved.title == "New Lab"