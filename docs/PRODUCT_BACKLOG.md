# Product Backlog – Student Assignment Tracker

---

## Product Backlog Table

| Story ID | User Story            | Priority (MoSCoW) | Effort (Story Points) | Dependencies |
| -------- | --------------------- | ----------------- | --------------------- | ------------ |
| US-001   | User Registration     | Must-have         | 3                     | None         |
| US-002   | User Login            | Must-have         | 3                     | US-001       |
| US-003   | Create Assignment     | Must-have         | 5                     | US-002       |
| US-004   | View Assignments      | Must-have         | 3                     | US-002       |
| US-007   | Track Deadlines       | Must-have         | 2                     | US-004       |
| US-009   | Receive Notifications | Should-have       | 3                     | US-007       |
| US-005   | Update Assignment     | Should-have       | 3                     | US-003       |
| US-006   | Delete Assignment     | Could-have        | 2                     | US-003       |
| US-008   | Mark as Completed     | Should-have       | 2                     | US-004       |
| US-010   | Manage Users          | Could-have        | 5                     | US-001       |
| US-011   | Data Security         | Must-have         | 5                     | US-002       |
| US-012   | System Performance    | Should-have       | 3                     | US-004       |

---

## Backlog Prioritization Justification

The prioritization of the backlog is based on delivering a **Minimum Viable Product (MVP)** that satisfies the most critical stakeholder needs.

* **Must-have stories** focus on core system functionality such as user authentication, assignment management, and data security. These are essential for the system to function.
* **Should-have stories** enhance usability and user experience, such as notifications and performance improvements.
* **Could-have stories** provide additional features that are useful but not critical for initial system deployment.

Effort estimates were assigned using the Fibonacci sequence (1, 2, 3, 5), reflecting the relative complexity of each user story.

Dependencies were identified to ensure logical implementation order, particularly for authentication and assignment-related features.

This prioritization ensures that the system delivers maximum value early while remaining scalable for future enhancements.
