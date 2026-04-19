# ✏️ Update Assignment Activity Diagram

```mermaid
flowchart TD

    A([Start]) --> B[Lecturer selects assignment]

    B --> C[Edit assignment details]

    C --> D{Are updated details valid?}

    D -->|No| E[Display validation error]
    E --> C

    D -->|Yes| F[Save updated assignment]

    F --> G[Update assignment in database]

    G --> H[Confirm update to lecturer]

    H --> I([End])

```
---

## 📌 Explanation

This activity diagram represents the process of updating an existing assignment by a lecturer.

### 🔄 Workflow Description

- The process begins when the lecturer selects an assignment to update.
- The lecturer edits the assignment details.
- The system validates the updated information.
- If invalid, an error message is displayed and the lecturer must correct the input.
- If valid, the updated assignment is saved and the database is updated.
- A confirmation message is displayed to the lecturer.

### 🔗 Traceability

- **Functional Requirements**
  - FR5: Assignment Updates

- **Use Cases**
  - UC5: Update Assignment

- **User Stories**
  - US-005: Update assignments

This workflow ensures that assignment updates are validated and correctly stored, maintaining data integrity within the system.
