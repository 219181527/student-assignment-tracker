# 📋 CHANGELOG

All notable changes to the **Student Assignment Tracker** project are documented here.

This file follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.

---

## [v1.1.0] — 2026-05-20

### Added — CI/CD Pipeline

- `.github/workflows/ci.yml` — GitHub Actions workflow with two jobs:
  - `Run Tests` — triggers on every push and every PR to `main`. Runs 395 tests across all layers with coverage reporting. Uploads `test-results.xml` and `coverage.xml` as artifacts. Blocks PR merge if any test fails
  - `Build Release Artifact` — triggers only on merge to `main`. Builds a Python wheel (`.whl`) and creates a versioned GitHub Release (`v1.0.{run_number}`) with release notes and the wheel attached
- `requirements.txt` — pinned dependency file used by CI for reproducible installs
- `PROTECTION.md` — documents all branch protection rules on `main` and justifies each rule

### Added — Branch Protection (main)

- Require pull request before merging — no direct pushes to `main`
- Require 1 approving review
- Dismiss stale reviews on new push
- Require status checks to pass (`Run Tests` job must be green)
- Require branches to be up to date before merging
- Do not allow bypassing rules (applies to admins)

### Fixed

- `actions/upload-artifact@v3` — deprecated, upgraded to `@v4`
- `setup-python cache: pip` — removed; caused failure when `requirements.txt` was missing. Added `requirements.txt` to fix

### Test Results (CI)

```
395 passed in 2.88s
80% coverage across all layers
```

---

## [v1.0.0] — 2026-05-18

### Added — Service Layer (`/services`)

- `services/base.py` — `BaseService` with shared validators and a typed exception hierarchy mapping to HTTP status codes: `NotFoundError` (404), `ValidationError` (422), `ConflictError` (409), `PermissionError` (403)
- `services/user_service.py` — `UserService` handling student/lecturer registration (duplicate email and student number prevention), login (credential + active account verification), and profile updates
- `services/assignment_service.py` — `AssignmentService` enforcing the full `DRAFT → PUBLISHED → CLOSED` lifecycle with ownership checks, inactive course prevention, and past due date validation
- `services/submission_service.py` — `SubmissionService` enforcing enrollment checks, one-submission-per-student rule, score range validation, re-grade prevention, and lecturer ownership on grading
- `tests/services/conftest.py` — Shared service test fixtures with isolated in-memory factory per test
- `tests/services/test_user_service.py` — 21 tests covering registration, login, profile management
- `tests/services/test_assignment_service.py` — 22 tests covering full assignment lifecycle
- `tests/services/test_submission_service.py` — 30 tests covering submission, grading, and retrieval

### Added — REST API (`/api`)

- `api/main.py` — FastAPI application with global exception handlers, OpenAPI metadata, and custom ReDoc route
- `api/schemas.py` — Pydantic v2 request/response schemas with `ConfigDict` and `json_schema_extra` for all 14 models
- `api/dependencies.py` — Cached `RepositoryFactory` with `lru_cache` and `dependency_overrides` support for test isolation
- `api/routes/users.py` — 9 endpoints: student/lecturer registration, login, get, list, update
- `api/routes/assignments.py` — 10 endpoints: create, get, list, update, delete, publish, close, list by course/lecturer, overdue
- `api/routes/submissions.py` — 6 endpoints: submit, get, list by assignment/student, grade, get grade
- `tests/api/test_api.py` — 30 integration tests end-to-end through the full stack

### Added — API Documentation (`/docs/api`)

- `docs/api/openapi.yaml` — Complete OpenAPI 3.1 specification (25 endpoints, all request/response schemas, all error responses)
- `docs/api/API_DOCS.md` — Human-readable endpoint reference with business rules and example workflows
- `docs/export_openapi.py` — Script to regenerate `openapi.json` and `openapi.yaml` from the live FastAPI app

### Fixed

- `DELETE /api/assignments/{id}` — Moved `lecturer_id` from request body to query parameter; `TestClient.delete()` does not support `json=` in newer httpx versions
- `api/schemas.py` — Replaced deprecated `Field(example=...)` with `model_config = ConfigDict(json_schema_extra=...)` — clears 34 Pydantic v2 deprecation warnings
- `api/main.py` — Added custom ReDoc HTML route to fix blank page caused by CDN load issues in default FastAPI setup

### Test Results

```
265 total tests passing
  73  service layer tests
  30  API integration tests
 192  repository + pattern tests (carried forward)
```

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
- `src/lecturer.py` — Added `from __future__ import annotations` and `TYPE_CHECKING` guard to resolve Pylance `"Assignment" is not defined` forward-reference warning (tracked in [#15](../../issues/15))
- `src/student.py` — Same `TYPE_CHECKING` fix applied for `Enrollment`, `Submission`, `Assignment`, `Notification` forward references

### GitHub Issues Raised

| Issue | Type | Title | Status |
|-------|------|-------|--------|
| [#15](../../issues/15) | 🐛 Bug | `lecturer.py` Pylance forward reference warning on `Assignment` return type | ✅ Closed — fixed via `TYPE_CHECKING` guard |
| [#16](../../issues/16) | 🐛 Bug | `sys.path.insert` in pattern files breaks pytest collection | ✅ Closed — fixed via `pytest.ini` and removed path hacks |
| [#17](../../issues/17) | ✨ Enhancement | Increase test coverage from 77% to 90%+ | 🔄 Open — `src/lecturer.py` at 64%, `src/enrollment.py` at 74% |

### Kanban Board Updates

- US-001 (User Registration) → **Done**
- US-002 (User Login) → **Done**
- US-003 (Create Assignment) → **Done**
- US-004 (View Assignments) → **Done**
- US-007 (Track Deadlines) → **Done**
- US-009 (Receive Notifications) → **In Progress** (unblocked — `NotificationService` implemented)
- US-010 (Manage Users) → **Done**

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