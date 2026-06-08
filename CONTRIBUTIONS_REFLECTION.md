# 🧠 Reflection — Cross-Project Contributions & Collaborative Development

**Contributor:** Mongameli Shasha (Student Number: 219181527)
**Course:** Postgraduate Diploma in ICT

---

## 1. Introduction

This reflection documents my engineering contributions, architectural
problem-solving, and collaboration workflows across multiple external peer
repositories during the Assignment 15 development cycle. Rather than
focusing on simple documentation adjustments, my contributions targeted
deep core logic implementations, domain entity mapping, circular dependency
decoupling, and error-handling standardization. This document outlines the
technical challenges encountered and lessons learned while working within
diverse backend architectures.

---

## 2. Deep Dive: Repository Contributions & Technical Case Studies

### A. Project 1: software-engineering-assignment
**Repository:** AkhonaHlongwa/software-engineering-assignment
**Feature Scope:** `refactor: standardize API global exception handlers and structural error payloads`
**Target Issue:** Issue #4 — Improve API Error handling responses

#### Technical Context & Diagnostic Verification

When evaluating the API layer of this repository, error handling across
the endpoints was implemented defensively but inconsistently. Several
routes caught raw system exceptions and leaked database tracebacks to the
client or returned generic `500 Internal Server Error` statuses for
predictable client-side input failures. This lacked clear RESTful feedback
protocols and breached basic security guidelines by exposing structural
internals.

#### Engineering Solutions Implemented

To establish a predictable, uniform interface response, I introduced a
unified global exception handling matrix utilizing FastAPI's middleware
validation layers:

- Built structural error schemas using Pydantic, ensuring that every
  intercepted error payload returns a standardized JSON structure with
  fields for timestamp, error code, client-readable message, and detailed
  fields
- Mapped specific domain error classes to their precise RESTful HTTP
  status code counterparts (e.g., converting item validation failures to
  `422 Unprocessable Entity` and parameter conflicts to `409 Conflict`)
- Cleaned out native try-except blocks from individual endpoint routes,
  delegating error intercept actions to an isolated application-wide
  handler to drastically improve codebase maintainability

#### Verification

Local execution trace tests verified that malformed requests are gracefully
captured, preventing container thread crashes and yielding clean, structured
error responses.

---

### B. Project 2: hospitality-management-system
**Repository:** Kamva-Ntlanga/hospitality-management-system
**Feature Scope:** `feat: implement US-006 housekeeping view/manage API routes and resolve circular imports`
**Target Issue:** Issue #6 — US-006: View and manage housekeeping tasks

#### Technical Context & Diagnostic Verification

This project required implementing a backend subsystem to track room
maintenance statuses, assign staff roles, and update housekeeping
conditions across diverse hotel floor configurations. The primary obstacle
encountered upon booting the application inside a local development
environment was a rigid circular dependency deadlock across the routing,
service, and database schema packages.

Because the housekeeping routes closely referenced room entity assignments,
and the room services conversely triggered automated cleaning dispatch
records, Python's runtime environment repeatedly failed to resolve module
objects during the application boot phase.

#### Engineering Solutions Implemented

To permanently unblock the framework, I reorganized the dependency graphs
by introducing decoupled interface references and abstracting internal
service definitions. I moved heavy cross-module imports directly into
local method scopes where runtime lookups occur, bypassing the global
scope imports that caused the initialization deadlock.

With the core architecture stabilized, I built out the endpoints for
US-006:

- Built robust `GET` endpoints utilizing specific database query parameters
  to filter active cleaning records based on urgency, assigned staff IDs,
  or room numbers
- Built secure `PATCH` routing matrices capable of altering structural
  enum matrices (`Clean`, `Dirty`, `Under-Maintenance`), ensuring that
  modifying a room's housekeeping status safely updates the master
  availability flag across the frontend dashboard

#### Verification

The resulting pull request effectively streamlined the application
workflow, providing an isolated, reliable API layer for the housekeeping
management system. CI pipeline passed in 23 seconds — screenshot included
in `MERGED_PRS.md`.

---

### C. Project 3: Smart Academic Library Assistance System (SALAS)
**Repository:** 211225347/Smart-Academic-Library-Assistance-System-SALAS-
**Feature Scope:** `feat(reservations): implement reservation domain models and business validation layer`
**Target Issue:** Issue #36 — Add Reservation API endpoints

#### Technical Context & Diagnostic Verification

The initial implementation of the SALAS platform contained stubbed REST
API placeholders within `api/main.py` that returned mock JSON objects to
simulate reservation tracking. Upon testing the environment locally inside
a GitHub Codespace using Uvicorn, the backend engine immediately suffered
runtime compilation and initialization crashes.

Tracing the traceback errors revealed that the core domain source
(`src/models.py`) had completely omitted critical structural classes
(`Reservation`, `Recommendation`, `AccountStatus`, `FineStatus`,
`ReservationStatus`) which were strictly expected by the contract
definitions in `repositories/interfaces.py` and the collection queries
inside `repositories/inmemory/inmemory_repositories.py`.

#### Engineering Solutions Implemented

To resolve these architectural gaps, I systematically expanded
`src/models.py` to establish the necessary domain properties, ensuring
that tracking parameters (such as `_student`, `_resource`, and unique
reservation positions) matched the expected query mechanics.

Once the data models compiled cleanly, I replaced the mock routes in
`api/main.py` with multi-layered business validation logic tied directly
to the `InMemoryReservationRepository`:

- **Shelf Availability Guard:** Implemented checks to intercept incoming
  payloads and explicitly reject reservations with an HTTP `400 Bad
  Request` if physical inventory count (`available_copies > 0`) is
  sitting unborrowed on the library shelves
- **Quota Cap Safeguard:** Designed transactional loops to scan current
  persistence files, capping student profiles to a maximum of 3 active
  pending or queued reservations
- **Dynamic Waitlist State Allocation:** Engineered logic to evaluate
  existing reservation sizes, dynamically computing queue metrics and
  routing overflow requests to a `ReservationStatus.QUEUED` state

#### Verification

Local terminal testing via detailed `curl` workflows confirmed that valid
identity records populate smoothly, while violating actions (such as
attempting to reserve an available item) are caught by the backend
validation engine to return precise error payloads.

---

## 3. Collaboration Reflections & Open-Source Challenges

### Maintaining Architecture Discipline & Style Alignment

The most significant lesson learned throughout this cross-project cycle
is the necessity of maintaining strict style discipline when contributing
to someone else's codebase. Dropping into systems authored by peers
requires a high level of code restraint.

Rather than rewriting existing patterns to match my own preferences, I
focused on learning their specific architectural idioms, variable casing
choices, and error handling behaviors. This discipline ensures that my
contributions look like a natural extension of their original code,
minimizing friction during peer code reviews.

### Resolving the "Works on My Machine" Dilemma in Cloud Environments

Developing software inside secure container environments like GitHub
Codespaces highlights the difference between localized hardware executions
and cloud-hosted deployments. Overcoming networking hurdles — such as
translating remote container bindings to accessible browser URLs during
the SALAS port configuration — showed that modern software engineering
requires a strong understanding of DevOps and network access policies
alongside traditional programming logic.

---

## 4. Conclusion

Participating in this cross-project development cycle provided a realistic
simulation of professional open-source collaboration. Diagnosing structural
runtime exceptions, resolving circular import deadlocks, and writing clean
domain-driven data guards highlighted the critical value of clear
programming contracts.

Ultimately, this assignment demonstrated how modular architecture patterns,
thorough documentation, and respectful peer communication allow independent
engineers to confidently build features together on a shared codebase.