# 🤝 Contributing to Student Assignment Tracker

Thank you for your interest in contributing! This guide covers everything
you need to get started — from setting up the project locally to submitting
a pull request.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Running Tests](#running-tests)
- [Picking an Issue](#picking-an-issue)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Commit Message Format](#commit-message-format)
- [Code of Conduct](#code-of-conduct)

---

## Prerequisites

Before you begin, make sure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.8+ | Primary language |
| Git | Any recent | Version control |
| pip | Latest | Package management |

---

## Local Setup

### 1. Fork the Repository

Click the **Fork** button at the top right of the repository page. This
creates your own copy of the project under your GitHub account.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/student-assignment-tracker.git
cd student-assignment-tracker
```

### 3. Add the Upstream Remote

```bash
git remote add upstream https://github.com/219181527/student-assignment-tracker.git
```

This lets you pull in future changes from the original repo.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify the Setup

```bash
# Run the full test suite — all 395 tests should pass
pytest tests/ -v
```

### 6. Run the API Locally

```bash
uvicorn api.main:app --reload
```

Open `http://localhost:8000/docs` to see the Swagger UI.

---

## Project Structure

```
src/                  ← Domain model classes (User, Student, Assignment, etc.)
creational_patterns/  ← Design pattern implementations
repositories/         ← Persistence layer (in-memory, filesystem, database stubs)
services/             ← Business logic (UserService, AssignmentService, etc.)
api/                  ← FastAPI REST endpoints and schemas
tests/                ← Full test suite
docs/                 ← API documentation and diagrams
```

---

## Coding Standards

### Style

- Follow **PEP 8** for all Python code
- Use **type hints** on all function signatures
- Keep lines under **100 characters**
- Use **descriptive variable names** — no single letters except loop counters

### Docstrings

All public classes and methods must have docstrings:

```python
def register_student(self, user_id: str, name: str, email: str) -> Student:
    """
    Register a new student account.

    Args:
        user_id: Unique identifier for the student
        name:    Full display name
        email:   Login email address

    Returns:
        The newly registered Student instance.

    Raises:
        ConflictError: If the email is already registered.
    """
```

### Architecture Rules

- **Domain classes** (`src/`) must not import from `services/` or `api/`
- **Services** must use repositories for all persistence — no direct domain
  object storage
- **API routes** must only call service methods — never repositories directly
- **Every new feature** must have corresponding unit tests

### Linting

Before submitting a PR, run:

```bash
# Check for style issues
pip install flake8
flake8 src/ services/ api/ --max-line-length=100

# Optional — auto-format
pip install black
black src/ services/ api/
```

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/services/test_user_service.py -v

# Run with coverage report
pytest tests/ -v --cov=src --cov=services --cov=api --cov-report=term-missing

# Run only tests matching a keyword
pytest tests/ -k "test_register" -v
```

All PRs must maintain or improve the current **80% coverage** threshold.

---

## Picking an Issue

1. Go to the [Issues tab](https://github.com/219181527/student-assignment-tracker/issues)
2. Filter by label:
   - 🟢 `good-first-issue` — Simple, well-defined tasks ideal for first-time contributors
   - 🔵 `feature-request` — Larger enhancements open for implementation
   - 🐛 `bug` — Confirmed bugs needing a fix
3. Comment on the issue: *"I'd like to work on this"* — this prevents duplicate effort
4. Wait for a maintainer to assign it to you before starting work

---

## Submitting a Pull Request

### 1. Create a Feature Branch

Always branch from `dev`, not `main`:

```bash
git checkout dev
git pull upstream dev
git checkout -b feature/your-feature-name
```

Branch naming convention:
- `feature/` — new functionality
- `fix/` — bug fixes
- `docs/` — documentation only
- `test/` — tests only

### 2. Make Your Changes

Write your code, add tests, update documentation if needed.

### 3. Run Tests Locally

```bash
pytest tests/ -v
```

All tests must pass before submitting.

### 4. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 5. Open a Pull Request

- Go to your fork on GitHub
- Click **"Compare & pull request"**
- Set base: `219181527/student-assignment-tracker` ← `dev`
- Fill in the PR template:
  - What does this PR do?
  - Which issue does it close? (`Closes #X`)
  - How was it tested?
- Submit and wait for review

### 6. Respond to Review Feedback

Maintainers may request changes. Push additional commits to the same branch —
the PR updates automatically.

---

## Commit Message Format

Follow the **Conventional Commits** standard:

```
<type>: <short description>

[optional body]
[optional footer: Closes #X]
```

| Type | When to use |
|------|------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `refactor` | Code restructuring without behaviour change |
| `ci` | CI/CD pipeline changes |
| `chore` | Maintenance tasks |

**Examples:**

```
feat: Add CourseService with enrollment management

fix: Prevent duplicate submissions on concurrent requests
Closes #42

docs: Add API authentication section to README

test: Add edge cases for GradeService score validation
```

---

## Code of Conduct

This project follows the
[Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

By participating, you agree to:
- Be respectful and inclusive in all interactions
- Accept constructive feedback graciously
- Focus on what is best for the community and project

Report unacceptable behaviour to the maintainer via GitHub.

---

## Questions?

Open a [GitHub Discussion](https://github.com/219181527/student-assignment-tracker/discussions)
or leave a comment on the relevant issue. We're happy to help!