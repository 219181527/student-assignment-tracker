# System Requirements – Student Assignment Tracker

## 1. Functional Requirements

The following functional requirements define the core capabilities of the system.

---

### FR1: User Registration

The system shall allow users (students and lecturers) to register accounts.

**Acceptance Criteria:**

* Users must provide a valid email and password
* The system must validate input fields before account creation

---

### FR2: User Authentication

The system shall allow users to log in securely.

**Acceptance Criteria:**

* Users must enter valid credentials
* The system must reject invalid login attempts

---

### FR3: Assignment Creation

The system shall allow lecturers to create assignments.

**Acceptance Criteria:**

* Lecturers must be able to input title, description, and due date
* The assignment must be saved in the database

---

### FR4: Assignment Viewing

The system shall allow students to view all available assignments.

**Acceptance Criteria:**

* Assignments must display title, description, and due date
* Data must be retrieved in real time

---

### FR5: Assignment Updates

The system shall allow lecturers to update assignment details.

---

### FR6: Assignment Deletion

The system shall allow lecturers to delete assignments.

---

### FR7: Deadline Tracking

The system shall allow students to track assignment deadlines.

**Acceptance Criteria:**

* Deadlines must be clearly displayed
* Overdue assignments must be indicated

---

### FR8: Submission Tracking

The system shall allow students to mark assignments as completed or submitted.

---

### FR9: Notifications

The system shall notify users of upcoming deadlines.

**Acceptance Criteria:**

* Notifications must be sent at least 24 hours before deadlines

---

### FR10: Role-Based Access Control

The system shall restrict access based on user roles (student or lecturer).

---

### FR11: Data Storage

The system shall store user and assignment data securely in a database.

---

## 2. Non-Functional Requirements

The following non-functional requirements define the quality attributes of the system.

---

### 2.1 Usability

**NFR1:** The system shall provide a user-friendly interface that allows users to navigate and perform tasks with minimal training.

**NFR2:** The system interface shall be responsive and accessible on both desktop and mobile devices.

---

### 2.2 Deployability

**NFR3:** The system shall be deployable on both Windows and Linux server environments.

---

### 2.3 Maintainability

**NFR4:** The system shall include clear documentation to support future maintenance and updates.

**NFR5:** The system shall be modular to allow independent updates to components without affecting the entire system.

---

### 2.4 Scalability

**NFR6:** The system shall support at least 1,000 concurrent users without performance degradation.

---

### 2.5 Security

**NFR7:** All user data shall be encrypted using industry-standard encryption methods.

**NFR8:** The system shall enforce role-based access control to protect sensitive data.

---

### 2.6 Performance

**NFR9:** The system shall load assignment data within 2 seconds under normal operating conditions.

**NFR10:** The system shall process user actions (e.g., login, assignment creation) within 3 seconds.
