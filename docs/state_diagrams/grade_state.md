# 🏆 Grade State Transition Diagram


```mermaid
stateDiagram-v2
    [*] --> Pending

    Pending --> Assigned : Lecturer grades submission

    Assigned --> Released : Grade visible to student

    Released --> Updated : Grade adjusted / remark

    Updated --> Finalized : Final grade confirmed

    Finalized --> Archived : Stored for records


```markdown

 ## 📌 Explanation

The Grade object represents the evaluation process of a student's submission, from initial grading to finalization and archival.

### 🔄 Key States

- **Pending**: The submission has not yet been graded
- **Assigned**: The lecturer has assigned a grade
- **Released**: The grade is visible to the student
- **Updated**: The grade is modified after review or remark
- **Finalized**: The grade is confirmed and cannot be changed
- **Archived**: The grade record is stored for future reference

### 🔗 Traceability

This object supports:

- **Functional Requirements**
  - FR8: Submission Tracking (grading follows submission)

- **Use Cases**
  - UC8: Mark as Completed / Submission process

- **User Stories**
  - US-008: Mark assignments as completed

Although grading is not explicitly defined as a standalone requirement, it is a natural extension of the submission process and is essential in academic systems for evaluating student performance.   