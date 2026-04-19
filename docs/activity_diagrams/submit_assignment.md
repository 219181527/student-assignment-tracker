# 📤 Submit Assignment Activity Diagram

```mermaid
flowchart TD

    A([Start]) --> B[Student selects assignment]

    B --> C[Upload / mark assignment as completed]

    C --> D{Before deadline?}

    D -->|Yes| E[Accept submission]

    D -->|No| F{Late submissions allowed?}

    F -->|Yes| G[Accept submission as late]
    F -->|No| H[Reject submission]

    E --> I[Store submission in database]
    G --> I

    I --> J[Update submission status]

    J --> K([End])

    H --> K

```
---

```markdown

## 📌 Explanation

This activity diagram represents the process of submitting an assignment within the system.

### 🔄 Workflow Description

- The process begins when the student selects an assignment.
- The student uploads the assignment or marks it as completed.
- The system checks whether the submission is before the deadline.
- If submitted on time, the submission is accepted.
- If late, the system checks if late submissions are allowed:
  - If allowed, the submission is accepted as late.
  - If not allowed, the submission is rejected.
- Accepted submissions are stored in the database and the status is updated.

### 🔗 Traceability

- **Functional Requirements**
  - FR8: Submission Tracking
  - FR7: Deadline Tracking (deadline check)

- **Use Cases**
  - UC8: Mark as Completed / Submit Assignment
  - UC7: Track Deadlines

- **User Stories**
  - US-008: Mark assignments as completed
  - US-007: Track deadlines

This workflow ensures proper handling of submissions, including deadline validation and late submission rules.
