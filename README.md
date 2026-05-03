# Student Assignment Tracker

## 📌 Project Overview

The **Student Assignment Tracker** is a software system designed to solve a common problem in higher education: students losing track of assignment deadlines across multiple courses, and lecturers lacking a structured platform for managing and distributing coursework.

The system provides:
- A centralised dashboard for students to view, filter, and monitor all assignment deadlines across enrolled courses
- A management interface for lecturers to create, publish, update, and close assignments
- Automated notifications triggered by deadlines, submissions, and grade releases
- A structured submission and grading pipeline with full status tracking

This project demonstrates a complete **Software Engineering lifecycle**, from requirements engineering and Agile planning through UML behavioural and structural modelling.

---

## 🌍 Domain

**Education Technology (EdTech)**

The system addresses the gap between institutional learning management systems (which are often overengineered) and informal tools like WhatsApp groups or paper planners (which offer no structure). The Student Assignment Tracker occupies the middle ground: lightweight, role-based, and deadline-focused.

---

## 🎯 Project Goals

| Goal | Description |
|------|-------------|
| Assignment Management | Lecturers can create, publish, update, and close assignments per course |
| Deadline Visibility | Students see all upcoming deadlines across enrolled courses in one place |
| Submission Tracking | Students can submit work and track submission and grading status |
| Notifications | System generates alerts for deadlines, submission confirmations, and grade releases |
| Role-Based Access | Students and lecturers see and do different things based on their role |

---

## ⚙️ Agile Project Management

This project applies **Agile (Scrum) principles** using GitHub:

* 📌 User Stories implemented as GitHub Issues
* 🏷️ Labels used for prioritisation and categorisation (Must-Have, Should-Have, Could-Have)
* 📊 Kanban Board used to track workflow and progress
* 🎯 Milestones used to define sprint goals
* 📅 Sprint Planning documented for development cycles

---

## 📊 Kanban Board

The project uses a **GitHub Kanban Board** to manage development tasks and visualise workflow.

### 🔧 Customisations

Two additional columns were added beyond the default GitHub template:

* **Testing** — Ensures features are verified before being marked complete, supporting quality assurance
* **Blocked** — Highlights tasks that cannot proceed due to dependencies or unresolved decisions, making bottlenecks visible early

### 📸 Board Overview

![Kanban Board](screenshots/kanban_board.png)

---

## 🛠️ Tools and Technologies

| Tool | Purpose |
|------|---------|
| Python 3.14 | Primary implementation language for all source classes and design patterns |
| pytest 9.x | Unit testing framework — 121 tests across 6 test modules |
| pytest-cov | Test coverage reporting — 77% coverage across `src/` and `creational_patterns/` |
| Markdown | All documentation and deliverables |
| Mermaid.js | UML diagrams (class, state, activity) embedded in Markdown |
| GitHub Issues | User story and task tracking |
| GitHub Projects (Kanban) | Workflow and sprint management |
| GitHub Milestones | Sprint goal definition |

---

## 📁 Repository Structure

```text
student-assignment-tracker
│
├── .gitignore
├── LICENSE
├── README.md
├── CHANGELOG.md
├── SPECIFICATION.md
├── ARCHITECTURE.md
├── pytest.ini
│
├── src/                               ← Class implementations (Assignment 10)
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── lecturer.py
│   ├── course.py
│   ├── assignment.py
│   ├── submission.py
│   ├── grade.py
│   ├── notification.py
│   └── enrollment.py
│
├── creational_patterns/               ← All 6 creational design patterns (Assignment 10)
│   ├── __init__.py
│   ├── simple_factory.py
│   ├── factory_method.py
│   ├── abstract_factory.py
│   ├── builder.py
│   ├── prototype.py
│   └── singleton.py
│
├── tests/                             ← Unit tests with coverage (Assignment 10)
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_simple_factory.py
│   ├── test_factory_method.py
│   ├── test_abstract_factory.py
│   ├── test_builder.py
│   ├── test_prototype.py
│   └── test_singleton.py
│
├── docs/
│   ├── STAKEHOLDERS.md
│   ├── REQUIREMENTS.md
│   ├── USE_CASES.md
│   ├── USE_CASE_SPECIFICATIONS.md
│   ├── TEST_CASES.md
│   ├── USER_STORIES.md
│   ├── PRODUCT_BACKLOG.md
│   ├── SPRINT_PLANNING.md
│   ├── TEMPLATE_ANALYSIS.md
│   ├── KANBAN_EXPLANATION.md
│   ├── KANBAN_REFLECTION.md
│   ├── REFLECTION.md
│   ├── USE_CASE_TEST_REFLECTION.md
│   ├── MODEL_INTEGRATION.md
│   ├── DOMAIN_MODEL.md
│   ├── CLASS_DIAGRAM.md
│   ├── CLASS_MODEL_REFLECTION.md
│   ├── state_diagrams/
│   └── activity_diagrams/
│
└── screenshots/
    └── kanban_board.png
```

---

## 📚 Documentation

### 📄 Core Documents

* [System Specification](./SPECIFICATION.md)
* [System Architecture](./ARCHITECTURE.md)

---

### 👥 Requirements Engineering

* [Stakeholder Analysis](./docs/STAKEHOLDERS.md)
* [System Requirements](./docs/REQUIREMENTS.md)

---

### 📊 Analysis & Design

* [Use Case Diagram & Description](./docs/USE_CASES.md)
* [Use Case Specifications](./docs/USE_CASE_SPECIFICATIONS.md)

---

### 🧪 Testing

* [Test Cases](./docs/TEST_CASES.md)

---

### 🚀 Agile Planning

* [User Stories](./docs/USER_STORIES.md)
* [Product Backlog](./docs/PRODUCT_BACKLOG.md)
* [Sprint Planning](./docs/SPRINT_PLANNING.md)

---

### 📊 Project Management

* [Template Analysis and Selection](./docs/TEMPLATE_ANALYSIS.md)
* [Kanban Board Explanation](./docs/KANBAN_EXPLANATION.md)
* [Kanban Reflection](./docs/KANBAN_REFLECTION.md)

---

## 🧩 System Modelling

### 🔄 Object State Diagrams

| Diagram | Description |
|---------|-------------|
| [Assignment State](./docs/state_diagrams/assignment_state.md) | DRAFT → PUBLISHED → CLOSED lifecycle |
| [User Account State](./docs/state_diagrams/user_account_state.md) | Registration, activation, suspension |
| [Submission State](./docs/state_diagrams/submission_state.md) | SUBMITTED → LATE → GRADED transitions |
| [Notification State](./docs/state_diagrams/notification_state.md) | UNREAD → READ delivery lifecycle |
| [Deadline Tracker State](./docs/state_diagrams/deadline_tracker_state.md) | Deadline proximity states |
| [Course State](./docs/state_diagrams/course_state.md) | Active/inactive course lifecycle |
| [Enrollment State](./docs/state_diagrams/enrollment_state.md) | ACTIVE → DROPPED → COMPLETED |
| [Grade State](./docs/state_diagrams/grade_state.md) | Grading and release lifecycle |

---

### 🔄 Activity Diagrams

| Diagram | Covers |
|---------|--------|
| [User Registration](./docs/activity_diagrams/user_registration.md) | FR1 |
| [User Login](./docs/activity_diagrams/user_login.md) | FR2 |
| [Create Assignment](./docs/activity_diagrams/create_assignment.md) | FR3 |
| [View Assignments](./docs/activity_diagrams/view_assignments.md) | FR4 |
| [Update Assignment](./docs/activity_diagrams/update_assignment.md) | FR5 |
| [Track Deadlines](./docs/activity_diagrams/track_deadlines.md) | FR7 |
| [Submit Assignment](./docs/activity_diagrams/submit_assignment.md) | FR8 |
| [Receive Notifications](./docs/activity_diagrams/receive_notifications.md) | FR9 |

---

## 💻 Implementation (Assignment 10)

### 🐍 Language Choice — Python 3.14

Python was chosen for its clean, readable syntax that maps directly to UML class diagrams, making the implementation-to-design traceability easy to verify. Python's `abc` module provides native abstract base class support for the Factory Method and Abstract Factory patterns, and `threading.Lock` enables production-grade thread safety in the Singleton.

### 📦 Source Classes (`/src`)

| Class | File | Key Responsibility |
|-------|------|--------------------|
| `User` | `user.py` | Base class — authentication, registration, profile |
| `Student` | `student.py` | Deadline tracking, assignment submission, enrollment access |
| `Lecturer` | `lecturer.py` | Assignment creation and lifecycle management |
| `Course` | `course.py` | Owns assignments, tracks enrollments |
| `Assignment` | `assignment.py` | DRAFT → PUBLISHED → CLOSED lifecycle, triggers notifications |
| `Submission` | `submission.py` | Late detection, grade association, notification trigger |
| `Grade` | `grade.py` | Score storage, percentage computation |
| `Notification` | `notification.py` | Typed alerts (DEADLINE, SUBMISSION, GRADE) |
| `Enrollment` | `enrollment.py` | Resolves Student ↔ Course many-to-many |

### 🧩 Creational Patterns (`/creational_patterns`)

| Pattern | Class | Justification |
|---------|-------|---------------|
| Simple Factory | `UserFactory` | Registration forms send a role string — one factory handles both `Student` and `Lecturer` creation without callers needing to import either subclass directly |
| Factory Method | `NotificationCreator` + 3 subclasses | Each trigger type builds a differently-worded notification — subclasses own their construction logic independently, following the Open/Closed Principle |
| Abstract Factory | `StudentDashboardFactory` / `LecturerDashboardFactory` | Students and lecturers see incompatible views of the same data — the factory guarantees compatible component families per role |
| Builder | `ConcreteAssignmentBuilder` + `AssignmentDirector` | Assignments have 9+ configurable fields — the builder prevents invalid half-built objects; the Director pre-wires quiz, essay, and project templates |
| Prototype | `AssignmentTemplateRegistry` | Recurring assignments (weekly labs) are cloned from a registered template — mutations on clones never affect the stored original |
| Singleton | `NotificationService` | One global dispatcher prevents duplicate alerts — double-checked locking ensures thread safety under concurrent requests |

### 🧪 Running Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src --cov=creational_patterns --cov-report=term-missing
```

**Results: 121 tests passed | 77% coverage**

---

### 🏗️ Domain & Class Modelling (Assignment 9)

* [Domain Model](./docs/DOMAIN_MODEL.md) — Core entities, typed attributes, relationships, and business rules
* [Class Diagram](./docs/CLASS_DIAGRAM.md) — Full UML class diagram with access modifiers, method signatures, and relationship types
* [Class Model Reflection](./docs/CLASS_MODEL_REFLECTION.md) — Critical analysis of design decisions and trade-offs

---

### 📌 Model Integration

* [Model Integration & Justification](./docs/MODEL_INTEGRATION.md)

---

## 👤 Author

**Mongameli Shasha**
Student Number: **219181527**
GitHub: [github.com/219181527](https://github.com/219181527)

---

