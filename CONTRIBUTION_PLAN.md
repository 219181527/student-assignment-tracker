# 📋 Contribution Plan — Cross-Project Collaboration

## Assignment 15: Cross-Project Contributions & Collaborative Development

---

## Overview

This document outlines my strategy for contributing to classmates'
repositories. The focus is on well-scoped contributions that follow each
project's guidelines, pass CI where available, and provide genuine
architectural value to each codebase.

**Contribution principles:**
- Comment on the issue before starting work to avoid duplication
- Keep PRs small and focused — one concern per PR
- Match the project's existing code style and conventions
- Always include tests where applicable
- Link every PR to its originating issue

---

## Selected Projects

### Project 1 — Software Engineering Assignment
**Repository:** `https://github.com/AkhonaHlongwa/software-engineering-assignment`
**CONTRIBUTING.md:** ✅ Present
**CI/CD:** ⚠️ Not configured

| Issue | Label | Type | My Plan |
|-------|-------|------|---------|
| Improve API Error handling responses (#4) | `good-first-issue` | Refactor | Standardize global exception handlers and structural error payloads using FastAPI middleware and Pydantic error schemas |

**Approach:** Introduce a unified global exception handling matrix. Map domain
error classes to precise HTTP status codes (422, 409, 404, 403). Remove
try-except blocks from individual routes and delegate all error interception
to an application-wide handler.

---

### Project 2 — Hospitality Management System
**Repository:** `https://github.com/Kamva-Ntlanga/hospitality-management-system`
**CONTRIBUTING.md:** ✅ Present
**CI/CD:** ✅ GitHub Actions configured — CI passing

| Issue | Label | Type | My Plan |
|-------|-------|------|---------|
| US-006: View and manage housekeeping tasks (#6) | `good-first-issue` | Feature | Implement housekeeping API routes and resolve circular import deadlock across routing, service, and schema packages |

**Approach:** Resolve circular dependency deadlock by moving cross-module
imports into local method scopes. Build `GET` endpoints for filtering
cleaning records by urgency and staff ID. Build `PATCH` endpoints for
updating room housekeeping status (`Clean`, `Dirty`, `Under-Maintenance`)
with master availability flag propagation.

---

### Project 3 — Smart Academic Library Assistance System (SALAS)
**Repository:** `https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-`
**CONTRIBUTING.md:** ✅ Present
**CI/CD:** ⚠️ Not configured

| Issue | Label | Type | My Plan |
|-------|-------|------|---------|
| Add Reservation API endpoints (#36) | `good-first-issue` | Feature | Implement reservation domain models, business validation logic, and replace mock API routes with real persistence-backed endpoints |

**Approach:** Expand `src/models.py` with missing domain classes
(`Reservation`, `ReservationStatus`, `AccountStatus`, `FineStatus`).
Replace stubbed routes in `api/main.py` with multi-layered validation:
shelf availability guard (reject if copies available), quota cap (max 3
active reservations per student), and dynamic waitlist allocation.

---

## Contribution Strategy

### Phase 1 — Refactoring and Standardization

Begin with `AkhonaHlongwa/software-engineering-assignment` — error
handling refactors are low-risk, high-visibility, and establish trust
with the maintainer before tackling more complex features.

### Phase 2 — Feature Implementation with CI

Tackle `Kamva-Ntlanga/hospitality-management-system` — this project has
a working CI pipeline, meaning contributions can be formally verified.
The circular import resolution needed to be done first before any new
feature work could be added.

### Phase 3 — Domain Architecture

Tackle `211225347/Smart-Academic-Library-Assistance-System-SALAS-` —
the deepest contribution, requiring domain model implementation from
scratch and full business validation logic.

---

## Risk Management

| Risk | Mitigation |
|------|-----------|
| CI not configured on some repos | Verify tests pass locally before pushing |
| Circular imports blocking development | Resolve at root before adding new code |
| Mock routes masking missing domain models | Trace runtime errors to source before patching |
| Style mismatch | Study existing code patterns before writing anything new |

---

## Success Criteria

| Target | Metric |
|--------|--------|
| PRs submitted | 3 ✅ |
| PRs merged | 3 minimum (10 marks each) |
| Feature PR bonus | 2 `enhancement`-level PRs (+5 marks each) |
| CI passing | 1/3 repos had CI — passing ✅ |