# 🧩 Class Diagram — Student Assignment Tracker

```mermaid
classDiagram

class User {
    +int userId
    +string name
    +string email
    +string password
    +string role
    +login()
    +logout()
    +register()
}

class Student {
    +viewAssignments()
    +submitAssignment()
    +trackDeadlines()
}

class Lecturer {
    +createAssignment()
    +updateAssignment()
    +deleteAssignment()
}

class Course {
    +int courseId
    +string courseName
    +string courseCode
    +addAssignment()
}

class Assignment {
    +int assignmentId
    +string title
    +string description
    +date dueDate
    +string status
    +publish()
    +close()
}

class Submission {
    +int submissionId
    +date submissionDate
    +string status
    +submit()
}

class Grade {
    +int gradeId
    +float score
    +string feedback
    +assignGrade()
}

class Notification {
    +int notificationId
    +string message
    +date sentDate
    +string status
    +sendNotification()
}

class Enrollment {
    +int enrollmentId
    +string status
}

User <|-- Student
User <|-- Lecturer

Lecturer "1" --> "0..*" Assignment : creates
Course "1" --> "0..*" Assignment : contains
Student "1" --> "0..*" Submission : submits
Assignment "1" --> "0..*" Submission : receives
Submission "1" --> "0..1" Grade : assigned
Student "1" --> "0..*" Notification : receives
Student "1" --> "0..*" Enrollment : has
Course "1" --> "0..*" Enrollment : includes

```
---

🧠 Explanation
Purpose

The class diagram expands on the domain model by showing:

System structure
Object responsibilities
Operations/methods
Relationships between classes
Key Design Features
Inheritance
Student and Lecturer inherit from User
Association
Lecturer creates assignments
Students submit assignments
Courses contain assignments
Encapsulation
Each class owns its own attributes and behavior
Traceability

Supports:

FR1 → Registration
FR2 → Login
FR3 → Assignment Creation
FR4 → Assignment Viewing
FR7 → Deadline Tracking
FR8 → Submission Tracking
FR9 → Notifications

---


