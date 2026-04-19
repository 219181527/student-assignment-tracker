# ⏰ Deadline Tracker State Transition Diagram

```mermaid
stateDiagram-v2
    [*] --> Monitoring

    Monitoring --> Upcoming : Deadline approaching (e.g., < 24 hours)

    Upcoming --> Due : Deadline reached

    Due --> Completed : Assignment submitted on time
    Due --> Overdue : No submission after deadline

    Overdue --> Closed : Submission no longer allowed

    Completed --> Archived : Task completed and stored

---

```markdown

## 📌 Explanation

The Deadline Tracker object represents how the system monitors and manages assignment deadlines to support student awareness and submission tracking.

### 🔄 Key States

- **Monitoring**: The system is tracking the assignment deadline
- **Upcoming**: The deadline is approaching (e.g., within 24 hours), triggering urgency
- **Due**: The deadline has been reached
- **Completed**: The assignment was submitted before or on the deadline
- **Overdue**: The assignment was not submitted on time
- **Closed**: The system prevents further submissions
- **Archived**: The deadline tracking record is stored for historical purposes

### 🔗 Traceability

This diagram aligns with:

- **Functional Requirements**
  - FR7: Deadline Tracking

- **Use Cases**
  - UC7: Track Deadlines

- **User Stories**
  - US-007: Track Deadlines

This ensures that deadline monitoring, overdue detection, and submission status tracking are clearly defined within the system.