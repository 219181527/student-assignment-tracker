# 👤 User Account State Transition Diagram

```mermaid
stateDiagram-v2
    [*] --> Registered

    Registered --> Active : Successful login (FR2 / UC2)
    Registered --> Suspended : Invalid login attempts

    Active --> LoggedOut : User logs out
    LoggedOut --> Active : User logs in again (FR2)

    Active --> Suspended : Policy violation / admin action (FR10)

    Suspended --> Active : Admin reactivates account (UC10)

    Active --> Deleted : Account removed by admin (UC10)

  
---


```markdown
## 📌 Explanation

The User Account object represents the lifecycle of a user within the system, from registration to possible deletion.

### 🔄 Key States

- **Registered**: The user has successfully created an account (FR1, UC1, US-001)
- **Active**: The user is logged in and can access the system (FR2, UC2, US-002)
- **LoggedOut**: The user has logged out but still has an active account
- **Suspended**: The account is temporarily restricted due to invalid login attempts or administrative action (FR10)
- **Deleted**: The account is permanently removed by an administrator (UC10, US-010)

### 🔗 Traceability

This diagram aligns with:

- **Functional Requirements**
  - FR1: User Registration
  - FR2: User Authentication
  - FR10: Role-Based Access Control

- **Use Cases**
  - UC1: Register Account
  - UC2: Login
  - UC10: Manage Users

- **User Stories**
  - US-001: Register account
  - US-002: User login
  - US-010: Manage users

This ensures that user authentication, access control, and account lifecycle management are clearly defined within the system.  