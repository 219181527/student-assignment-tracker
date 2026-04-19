# 📤 Submission State Transition Diagram

```mermaid
stateDiagram-v2
    [*] --> NotSubmitted

    NotSubmitted --> Submitted : Student submits assignment (FR8 / UC8)

    Submitted --> Late : Submitted after deadline (FR7)
    Submitted --> UnderReview : Lecturer reviews submission

    UnderReview --> Graded : Marks assigned

    Graded --> Archived : Stored for records

  
---

```markdown
## 📌 Explanation

The Submission object represents the lifecycle of a student's assignment submission, from initial state to final grading and archival.

### 🔄 Key States

- **NotSubmitted**: The student has not yet submitted the assignment
- **Submitted**: The assignment has been submitted by the student (FR8, UC8, US-008)
- **Late**: The submission was made after the deadline (FR7, UC7, US-007)
- **UnderReview**: The lecturer is reviewing the submission
- **Graded**: The submission has been evaluated and marks assigned
- **Archived**: The submission is stored for record-keeping

### 🔗 Traceability

This diagram aligns with:

- **Functional Requirements**
  - FR7: Deadline Tracking
  - FR8: Submission Tracking

- **Use Cases**
  - UC7: Track Deadlines
  - UC8: Mark as Completed / Submit Assignment

- **User Stories**
  - US-007: Track deadlines
  - US-008: Mark assignments as completed

This ensures that submission handling, deadline enforcement, and grading processes are clearly modeled within the system.  