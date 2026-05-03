# 📋 CHANGELOG

All notable changes to the **Student Assignment Tracker** project are documented here.

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.

---

## [Assignment 10] — 2026-05-04

### Added — Class Implementation (`/src`)

- `src/user.py` — Base `User` class with SHA-256 password hashing, `register()`, `login()`, `logout()`, and `update_profile()` methods
- `src/student.py` — `Student` subclass with `view_assignments()`, `submit_assignment()`, `track_deadlines()`, and `get_enrollments()`. Enforces active-enrollment check before returning assignment data
- `src/lecturer.py` — `Lecturer` subclass with `create_assignment()`, `update_assignment()`, `delete_assignment()`, `view_submissions()`. Ownership checks on all mutating operations
- `src/course.py` — `Course` class owning assignments (composition) and tracking enrollments (aggregation)
- `src/assignment.py` — `Assignment` class with guarded `DRAFT → PUBLISHED → CLOSED` status transitions. `publish()` auto-triggers deadline notifications to enrolled students
- `src/submission.py` — `Submission` class with late detection at construction time. Grading triggers a `GRADE` notification automatically
- `src/grade.py` — `Grade` class with `get_percentage(total_marks)` derived computation
- `src/notification.py` — `Notification` class with `triggerType` validated against `DEADLINE | SUBMISSION | GRADE` enum
- `src/enrollment.py` — `Enrollment` class resolving the Student ↔ Course many-to-many. Self-registers with both `Student` and `Course` on construction
- `src/__init__.py` — Package file exposing all 9 classes

### Added — Creational Patterns (`/creational_patterns`)

- `simple_factory.py` — `UserFactory.create_user(role, ...)` creates `Student` or `Lecturer` from a role string. Role lookup is case-insensitive. Raises `ValueError` on unknown roles
- `factory_method.py` — Abstract `NotificationCreator` with three concrete subclasses: `DeadlineNotificationCreator`, `SubmissionNotificationCreator`, `GradeNotificationCreator`. Each builds a differently-worded, typed notification
- `abstract_factory.py` — `DashboardFactory` interface with `StudentDashboardFactory` and `LecturerDashboardFactory` producing compatible families of `AssignmentView`, `SubmissionSummary`, and `NotificationPanel` components
- `builder.py` — `ConcreteAssignmentBuilder` with method chaining and full input validation. `AssignmentDirector` pre-wires three named templates: quiz (30 marks, 2 days), essay (100 marks, 14 days), project (150 marks, 30 days)
- `prototype.py` — `AssignmentTemplate` with `clone()` (shallow) and `deep_clone()` (deep copy). `AssignmentTemplateRegistry` stores named templates and always returns deep clones — mutations on clones never affect the registry
- `singleton.py` — Thread-safe `NotificationService` using double-checked locking. Provides `enqueue()`, `dispatch_all()`, `dispatch_to()`, `get_stats()`, and `get_log()`. Verified safe across 20 concurrent threads

### Added — Unit Tests (`/tests`)

- `tests/conftest.py` — Shared pytest fixtures: `lecturer`, `student`, `student_b`, `course`, `enrolled_student`, `assignment`, `submission`, `graded_submission`. `autouse` fixture resets `NotificationService` state before every test
- `tests/test_simple_factory.py` — 13 tests covering student creation, lecturer creation, role case-insensitivity, unknown role handling, and password hashing verification
- `tests/test_factory_method.py` — 16 tests covering all three notification creator types, message content, trigger types, uniqueness per student, and error on ungraded submission
- `tests/test_abstract_factory.py` — 19 tests covering component type correctness per factory, rendered output content, empty state handling, family compatibility, and `render_dashboard` role-agnostic client
- `tests/test_builder.py` — 22 tests covering attribute setting, method chaining, builder reset after build, all edge cases (empty title, past date, zero/negative marks), and all three Director templates
- `tests/test_prototype.py` — 15 tests covering shallow vs deep clone independence, registry retrieval, mutation isolation, unknown key error, and `to_assignment_dict()` output shape
- `tests/test_singleton.py` — 16 tests covering instance identity, shared state across references, queue/dispatch lifecycle, audit log, per-type statistics, reset behaviour, and thread safety with 20 concurrent threads

### Added — Configuration

- `pytest.ini` — Sets `pythonpath = .` and `testpaths = tests` so pytest resolves all imports from the repo root without manual `sys.path` manipulation

### Fixed

- Removed `sys.path.insert` hacks from all pattern files — imports now resolve correctly when run as a package from the repo root
- `creational_patterns/__init__.py` — Removed eager imports that caused `ImportError` during pytest collection. Patterns are now imported directly from their modules
- `src/lecturer.py` — Added `from __future__ import annotations` and `TYPE_CHECKING` guard to resolve Pylance `"Assignment" is not defined` forward-reference warning
- `src/student.py` — Same `TYPE_CHECKING` fix applied for `Enrollment`, `Submission`, `Assignment`, `Notification` forward references

### Test Results

```
121 passed in 10.70s
Coverage: 77% across src/ and creational_patterns/
```

| File | Statements | Missed | Coverage |
|------|-----------|--------|----------|
| src/submission.py | 44 | 2 | 95% |
| src/notification.py | 33 | 4 | 88% |
| src/student.py | 53 | 9 | 83% |
| src/user.py | 46 | 10 | 78% |
| src/enrollment.py | 38 | 10 | 74% |
| src/grade.py | 35 | 10 | 71% |
| src/lecturer.py | 44 | 16 | 64% |
| **TOTAL** | **838** | **194** | **77%** |

---

## [Assignment 9] — 2026-04-27

### Added

- `docs/DOMAIN_MODEL.md` — Full domain model with 8 typed entities, enum-valued attributes, business rules, and relationship summary table. `Enrollment` resolves the Student ↔ Course many-to-many. `Notification` linked to both `Assignment` and `Submission` as trigger sources
- `docs/CLASS_DIAGRAM.md` — Mermaid.js class diagram with private attributes, typed method signatures, and correct UML relationship types (composition `*--`, aggregation `o--`, association `-->`, inheritance `<|--`)
- `docs/CLASS_MODEL_REFLECTION.md` — 950+ word critical reflection covering abstraction challenges, many-to-many resolution, composition vs aggregation trade-offs, alignment with FR/UC/state diagrams from prior assignments, and OO lessons learned

### Updated

- `README.md` — Added Assignment 9 section with links, tools table, improved project goals table, and submission checklist

---

## [Assignment 8] — 2026-04-20

### Added

- State diagrams for: Assignment, User Account, Submission, Notification, Deadline Tracker, Course, Enrollment, Grade
- Activity diagrams for: User Registration, Login, Create Assignment, View Assignments, Update Assignment, Track Deadlines, Submit Assignment, Receive Notifications
- `docs/MODEL_INTEGRATION.md` — Justification of how behavioural models align with requirements and use cases

---

## [Assignment 6] — 2026-04-06

### Added

- `docs/USER_STORIES.md` — User stories in Gherkin-style format
- `docs/PRODUCT_BACKLOG.md` — Prioritised backlog with MoSCoW labels
- `docs/SPRINT_PLANNING.md` — Sprint 1 and Sprint 2 planning documentation
- GitHub Kanban board with custom **Testing** and **Blocked** columns
- GitHub Milestones for sprint goals
- GitHub Issues for all user stories with labels

---

## [Assignment 5] — 2026-03-30

### Added

- `docs/USE_CASES.md` — Use case diagram and descriptions (UC1–UC9)
- `docs/USE_CASE_SPECIFICATIONS.md` — Detailed specifications with preconditions, postconditions, and alternate flows
- `docs/TEST_CASES.md` — Test cases mapped to use cases

---

## [Assignment 4] — 2026-03-23

### Added

- `docs/STAKEHOLDERS.md` — Stakeholder analysis with roles, interests, and influence
- `docs/REQUIREMENTS.md` — Functional (FR1–FR9) and non-functional requirements
- `SPECIFICATION.md` — System specification document
- `ARCHITECTURE.md` — High-level system architecture