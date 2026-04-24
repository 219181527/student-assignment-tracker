# 🧠 Reflection — Domain Model and Class Diagram

## 📌 Introduction

This reflection discusses the development of the Domain Model and Class Diagram for the Student Assignment Tracker system.

These models were created to represent the structure of the system and the relationships between key entities. They also support understanding of how the system is organized before implementation.

---

## 🧩 Domain Model Reflection

The Domain Model helped identify the major entities within the Student Assignment Tracker system.

The main entities selected were:

* User
* Student
* Lecturer
* Course
* Assignment
* Submission
* Grade
* Notification
* Enrollment

These entities were chosen because they represent the core concepts within the problem domain.

The domain model allowed relationships between entities to be visualized clearly. For example:

* A lecturer creates assignments
* Students submit assignments
* Courses contain assignments
* Students enroll in courses

This improved understanding of how data flows within the system.

---

## 🏗️ Class Diagram Reflection

The Class Diagram expanded on the Domain Model by introducing:

* Attributes
* Methods
* Object responsibilities
* Inheritance relationships

The `User` class was generalized to avoid duplication between Student and Lecturer entities.

Inheritance was used to demonstrate object-oriented design principles.

The class diagram provided a more technical representation of the system and showed how objects may behave during implementation.

---

## 🔗 Relationship Between Models

The Domain Model and Class Diagram complement each other.

* The Domain Model focuses on conceptual entities.
* The Class Diagram focuses on implementation structure.

Together, they create a strong system design foundation.

---

## 🎯 Challenges Encountered

One challenge was determining the correct relationships between entities.

For example:

* Whether Enrollment should be modeled separately
* How Submission connects to Grade
* Ensuring multiplicity was realistic

These challenges were solved by revisiting functional requirements and user stories.

---

## 📚 Learning Outcome

This activity improved understanding of:

* Object-oriented modeling
* UML relationships
* Entity identification
* System decomposition
* Software design principles

It also demonstrated how conceptual models evolve into technical designs.

---

## ✅ Conclusion

The Domain Model and Class Diagram provided a clear representation of the Student Assignment Tracker system.

These models ensure that:

* System structure is well defined
* Relationships are documented
* Object responsibilities are clear
* The design supports future implementation

This modeling process strengthened the overall software engineering design of the project.
