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
├── SPECIFICATION.md
├── ARCHITECTURE.md
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
│   │
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

### 🏗️ Domain & Class Modelling 

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

