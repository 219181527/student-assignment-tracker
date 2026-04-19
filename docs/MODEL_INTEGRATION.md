# 📊 Model Integration & Justification

## 📌 Overview

This document explains how the different system models developed in Assignment 8 (Object State Diagrams and Activity Diagrams) integrate with previous artefacts, including functional requirements, use cases, and user stories.

The goal is to demonstrate consistency, traceability, and completeness in the system design.

---

## 🔗 Integration with Functional Requirements

The models were developed directly from the system’s functional requirements:

* **FR1 & FR2 (User Management)**
  → Represented in *User Account State Diagram* and *Login/Registration Activity Diagrams*

* **FR3–FR6 (Assignment Management)**
  → Represented in *Assignment State Diagram* and *Create/Update Activity Diagrams*

* **FR7 (Deadline Tracking)**
  → Represented in *Deadline Tracker State Diagram* and *Track Deadlines Activity Diagram*

* **FR8 (Submission Tracking)**
  → Represented in *Submission State Diagram* and *Submit Assignment Activity Diagram*

* **FR9 (Notifications)**
  → Represented in *Notification State Diagram* and *Receive Notifications Activity Diagram*

This ensures that every functional requirement is supported by at least one system model.

---

## 🔗 Integration with Use Cases

Each activity diagram directly corresponds to a use case:

* UC1 → User Registration
* UC2 → Login
* UC3 → Create Assignment
* UC4 → View Assignments
* UC5 → Update Assignment
* UC7 → Track Deadlines
* UC8 → Submit Assignment
* UC9 → Receive Notifications

This alignment ensures that user interactions are fully modeled through system workflows.

---

## 🔗 Integration with User Stories

All diagrams were aligned with the user stories developed in Assignment 6:

* Student actions (view, submit, track deadlines)
* Lecturer actions (create, update, delete assignments)
* System actions (notifications, validation, tracking)

This ensures that the system behavior reflects real user needs.

---

## 🧩 Design Justification

### 1. Choice of Objects

The following objects were selected:

* User Account
* Assignment
* Submission
* Notification
* Course
* Enrollment
* Deadline Tracker
* Grade

These objects represent the **core entities** of the system and cover:

* User management
* Assignment lifecycle
* Submission and evaluation
* System automation (notifications, deadlines)

---

### 2. State Diagrams

State diagrams were used to model **object lifecycles**, showing how system entities change over time.

This helps in:

* Understanding system behavior
* Defining valid transitions
* Preventing invalid states

---

### 3. Activity Diagrams

Activity diagrams were used to model **user workflows and system processes**, including:

* Input validation
* Decision-making
* Loops (retry, monitoring)
* System responses

This ensures clarity in how the system operates.

---

### 4. Consistency Across Models

The system models are consistent because:

* The same terminology is used across all diagrams
* All workflows align with defined requirements
* Objects and processes are interconnected

---

## 🎯 Conclusion

The combination of state diagrams and activity diagrams provides a comprehensive view of both:

* **Static behavior** (object states)
* **Dynamic behavior** (system workflows)

This ensures that the Student Assignment Tracker system is:

* Well-structured
* Fully traceable
* Aligned with user needs
* Ready for implementation

---

## ✅ Summary

* All functional requirements are covered
* All major use cases are modeled
* All user stories are represented
* The system design is consistent and complete

This demonstrates a high-quality Software Engineering design process.
