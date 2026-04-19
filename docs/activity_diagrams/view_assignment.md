# 👀 View Assignments Activity Diagram

```mermaid
flowchart TD

    A([Start]) --> B[User logs into system]

    B --> C[Request assignment list]

    C --> D[Retrieve assignments from database]

    D --> E{Assignments available?}

    E -->|No| F[Display "No assignments available"]
    F --> G([End])

    E -->|Yes| H[Display assignment list]

    H --> I([End])

```
---

```markdown
## 📌 Explanation

This activity diagram represents the process of viewing assignments within the system.

### 🔄 Workflow Description

- The process begins when the user logs into the system.
- The user requests to view available assignments.
- The system retrieves assignment data from the database.
- If no assignments are available, a message is displayed.
- If assignments exist, they are displayed to the user.

### 🔗 Traceability

- **Functional Requirements**
  - FR4: Assignment Viewing

- **Use Cases**
  - UC4: View Assignments

- **User Stories**
  - US-004: View assignments

This workflow ensures that assignment data is retrieved and displayed efficiently, providing users with real-time access to academic tasks.
---