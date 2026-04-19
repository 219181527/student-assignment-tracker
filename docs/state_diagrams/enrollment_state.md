# 🧾 Enrollment State Transition Diagram

```mermaid
stateDiagram-v2
    [*] --> Requested

    Requested --> Enrolled : Enrollment approved
    Requested --> Rejected : Enrollment denied

    Enrolled --> Dropped : Student withdraws

    Enrolled --> Completed : Course finished

    Completed --> Archived : Stored for records
    Dropped --> Archived : Stored for records

---

```markdown

## 📌 Explanation

The Enrollment object represents the lifecycle of a student’s participation in a course, from initial request to completion or withdrawal.

### 🔄 Key States

- **Requested**: The student has requested enrollment in a course
- **Enrolled**: The student is successfully enrolled and can access course content
- **Rejected**: The enrollment request is denied
- **Dropped**: The student withdraws from the course
- **Completed**: The student finishes the course
- **Archived**: The enrollment record is stored for future reference

### 🔗 Traceability

This object supports:

- **Functional Requirements**
  - FR4: Assignment Viewing (students must be enrolled to access assignments)

- **Use Cases**
  - UC4: View Assignments

- **User Stories**
  - US-004: View assignments

Although enrollment is not explicitly listed as a functional requirement, it is essential for controlling access to course content and ensuring that only authorized students can view assignments.