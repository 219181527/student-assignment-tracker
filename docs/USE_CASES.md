# Use Case Diagram – Student Assignment Tracker

## Use Case Diagram (Mermaid)

```mermaid
flowchart LR

%% Actors
Student([Student])
Lecturer([Lecturer])
Admin([System Administrator])
IT([IT Support])
UniAdmin([University Administration])
LMS([External LMS])

%% Use Cases
UC1((Register Account))
UC2((Login))
UC3((Create Assignment))
UC4((View Assignments))
UC5((Update Assignment))
UC6((Delete Assignment))
UC7((Track Deadlines))
UC8((Mark as Completed))
UC9((Receive Notifications))
UC10((Manage Users))

%% Relationships
Student --> UC1
Student --> UC2
Student --> UC4
Student --> UC7
Student --> UC8
Student --> UC9

Lecturer --> UC2
Lecturer --> UC3
Lecturer --> UC5
Lecturer --> UC6

Admin --> UC10

IT --> UC10

UniAdmin --> UC4

LMS --> UC4
LMS --> UC9
```

## Explanation

### Key Actors and Roles

* **Student**: Interacts with the system to view assignments, track deadlines, and mark tasks as completed.
* **Lecturer**: Responsible for creating, updating, and deleting assignments.
* **System Administrator**: Manages users and system access.
* **IT Support Staff**: Maintains system functionality and supports user management.
* **University Administration**: Monitors academic progress and assignment data.
* **External LMS**: Integrates with the system to provide assignment data and notifications.

---

### Relationships Between Actors and Use Cases

* Students interact with core use cases such as viewing assignments and tracking deadlines.
* Lecturers are responsible for managing assignment lifecycle (create, update, delete).
* The "Receive Notifications" use case is indirectly supported by the LMS system.
* The "Manage Users" use case is shared between System Administrator and IT Support.

---

### Alignment with Stakeholder Concerns

* Students' need for organization is addressed through "Track Deadlines" and "Receive Notifications."
* Lecturers' need for efficiency is supported by assignment management use cases.
* IT and administrators’ concerns about system control are handled via "Manage Users."
* Integration with LMS ensures data consistency and reduces duplication.

This ensures the system meets both functional requirements and stakeholder expectations defined in Assignment 4.
