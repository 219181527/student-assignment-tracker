# 🧠 Reflection — Domain Model and Class Diagram

## 📌 Introduction

Developing the Domain Model and Class Diagram for the Student Assignment Tracker was the most structurally demanding part of this project so far. Unlike the use cases and activity diagrams from earlier assignments, which described *what* the system does and *how* it flows, these models required me to define *what the system is made of* — its core entities, their internal structure, and the precise nature of every relationship between them. This shift from behavioural to structural thinking exposed gaps in my earlier understanding and forced several important design decisions.

---

## 🧩 Challenges in Designing the Domain Model

### Abstraction and Entity Identification

The first challenge was deciding what constitutes a *domain entity* versus an attribute or a derived concept. My initial model included a `Deadline` class, treating submission cutoffs as a first-class entity. After revisiting FR7 (Deadline Tracking), I realised that a deadline is a property of an `Assignment`, not an independent entity — it carries no relationships of its own and has no lifecycle. Collapsing it into `Assignment.dueDate` simplified the model without losing any domain meaning.

A similar problem arose with `Notification`. Early on it had no source — it existed as a standalone entity with no connection to what triggered it. This made it impossible to trace *why* a notification was sent, which contradicted FR9 (Notifications). The fix was to add a `triggerType` attribute and associate `Notification` with both `Assignment` (for deadline alerts) and `Submission` (for confirmation and grade alerts). This small change made the entity far more meaningful and directly traceable to requirements.

### The Many-to-Many Problem

Modeling the relationship between `Student` and `Course` proved harder than expected. A naive approach — a direct many-to-many association — loses important information: when did the student enroll? Are they still active? Can they drop the course? Promoting `Enrollment` to a full entity with its own attributes (`enrollmentDate`, `status`) and methods (`drop()`, `complete()`) resolved this cleanly. It also aligned with the business rule that only *actively enrolled* students should be able to view course assignments — a rule that cannot be enforced on a bare association.

---

## 🏗️ Challenges in Designing the Class Diagram

### Choosing the Right Relationship Types

The most technically difficult part of the class diagram was distinguishing between composition, aggregation, and association. These are conceptually close but carry different semantic weight. I initially used plain association (`-->`) for all relationships, which is the most common mistake in UML class diagrams.

Revisiting each relationship individually forced clearer thinking:

- **Composition (`*--`)** was appropriate for `Course → Assignment` and `Assignment → Submission` because neither child entity has meaning outside its parent. An assignment without a course, or a submission without an assignment, is orphaned data.
- **Aggregation (`o--`)** was used for `Student → Enrollment` and `Course → Enrollment` because an enrollment record could theoretically persist even if a student's account were suspended — it represents a historical fact about participation.
- **Association (`-->`)** was used for `Lecturer → Assignment` because the lecturer is not the container of assignments; the course is. The lecturer's relationship is one of *authorship*, not ownership.

Making these distinctions took considerably more time than initially expected, but it produced a more honest and implementation-ready diagram.

### Method Signatures

Adding typed parameters and return types to every method was tedious but valuable. It forced me to think through what each operation actually needs to know and what it produces. For example, `isOverdue() Boolean` is a derived method that the `Assignment` class can compute internally from `dueDate` — it requires no parameters. By contrast, `getPercentage(totalMarks: int) float` in `Grade` requires an external input because the assignment's total mark is not stored on the grade itself. Working through these signatures surfaced a potential design flaw: `Grade` does not hold a reference to the `Assignment` it belongs to, only to the `Submission`. This is technically sufficient (Submission links to Assignment), but it means computing a percentage requires traversing two relationships. This is a trade-off I accepted to avoid redundant foreign keys.

---

## 🔗 Alignment With Prior Assignments

### Requirements (Assignment 4)

Every class in the diagram is traceable to at least one functional requirement. The `User` inheritance hierarchy satisfies FR1 (Registration) and FR2 (Authentication). The `Assignment`, `Submission`, and `Grade` chain satisfies FR3, FR8, and implicitly FR7. The `Notification` class with its trigger associations satisfies FR9. No class exists in the diagram without a corresponding requirement — and no requirement was left without a corresponding class.

### Use Cases (Assignment 5)

The use cases defined in Assignment 5 map directly onto class methods. UC3 (Create Assignment) is implemented as `Lecturer.createAssignment()`. UC8 (Submit Assignment) maps to `Student.submitAssignment()`. UC9 (Receive Notifications) maps to `Notification.send()` and `Notification.markAsRead()`. This one-to-one traceability confirmed that the class diagram is behaviourally complete relative to the use case model.

### State and Activity Diagrams (Assignment 8)

The state diagram for `Assignment` (DRAFT → PUBLISHED → CLOSED) informed the `status` attribute and the `publish()` and `close()` methods directly. Similarly, the activity diagram for the submission flow confirmed that `Submission` needs an `isLate()` method — a step that was modelled as a decision node in the activity diagram but needed to become executable logic in the class diagram.

---

## ⚖️ Trade-offs Made

**Inheritance vs. composition for User:** Using inheritance (`Student extends User`, `Lecturer extends User`) is clean but creates a rigid hierarchy. If a user needed to be both a student and a lecturer simultaneously, this model would break. A role-based approach using composition (a `User` has a collection of `Role` objects) would be more flexible. I chose inheritance because the system requirements do not anticipate dual-role users, and inheritance keeps the model simpler and more readable for this scope.

**Enrollment as an entity vs. a join table:** Promoting `Enrollment` to a full class adds complexity but captures business state that a simple join table cannot. The trade-off is justified because enrollment status is a domain concept, not just a database concern.

**Notification as a passive entity:** Notifications are modelled as data objects rather than as a service. A `NotificationService` class would be more architecturally correct for a layered design, but this level of design belongs in the implementation phase, not the domain or class model.

---

## 📚 Lessons Learned

This assignment reinforced that **UML is a thinking tool, not just a documentation tool**. The process of drawing the class diagram forced decisions that would otherwise have been deferred to implementation — and by then, they are far more expensive to change. The distinction between composition and aggregation, for instance, has direct implications for database schema design (cascade deletes), which would have caused bugs if left unresolved.

It also highlighted how **each model in the software engineering process feeds into the next**. The requirements shaped the entities, the use cases shaped the methods, and the state diagrams shaped the attribute enumerations. Working backwards from the class diagram to check alignment with earlier deliverables was the most valuable quality-assurance step in this assignment.

---

## ✅ Conclusion

The Domain Model and Class Diagram for the Student Assignment Tracker represent a complete structural specification of the system. The challenges encountered — from resolving many-to-many relationships, to distinguishing relationship types, to writing honest method signatures — all produced better design decisions than the initial draft. The process confirmed that careful structural modelling before implementation reduces ambiguity, prevents architectural mistakes, and ensures that every feature in the requirements has a clear home in the codebase.