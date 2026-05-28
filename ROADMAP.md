# 🗺️ Project Roadmap — Student Assignment Tracker

This roadmap outlines planned features and improvements for the Student
Assignment Tracker. Items are grouped by priority and complexity to help
contributors pick work that matches their skill level.

Community contributions are welcome on any item marked with 🤝.

---

## ✅ Completed

| Feature | Description |
|---------|-------------|
| Domain Model | 9 core entities with typed attributes and business rules |
| Creational Patterns | 6 design patterns applied to real domain problems |
| Repository Layer | In-memory, filesystem, and database stub backends |
| Service Layer | UserService, AssignmentService, SubmissionService |
| REST API | 25 FastAPI endpoints with Swagger/OpenAPI documentation |
| CI/CD Pipeline | GitHub Actions — automated testing and release artifacts |
| Branch Protection | PR reviews and status checks required on `main` |

---

## 🔜 Short Term (Next Release)

### Authentication & Security
- [ ] 🤝 **JWT Authentication** — Replace role-based ID passing with proper
  JWT tokens. Issue `#good-first-issue` — implement `POST /api/auth/token`
  endpoint and token validation middleware
- [ ] 🤝 **Password Reset** — Add `POST /api/users/reset-password` endpoint
  with email token flow
- [ ] **Rate Limiting** — Add per-IP rate limiting to prevent API abuse
  using `slowapi`

### Course Management
- [ ] 🤝 **CourseService** — Implement full CRUD for courses via the API.
  Currently courses are added directly via the repository — expose them
  through a proper service and endpoints
- [ ] 🤝 **Enrollment Endpoint** — Add `POST /api/enrollments` so students
  can enroll in courses via the API rather than directly via the factory

### Testing
- [ ] 🤝 **Increase Coverage to 90%+** — `src/lecturer.py` is at 64%,
  `src/enrollment.py` at 74%. Add edge case tests for `delete_assignment()`
  and `drop()` / `complete()` enrollment transitions

---

## 🔮 Medium Term

### Persistence
- [ ] **SQLite Database Backend** — Implement `DatabaseStudentRepository`
  and friends using SQLAlchemy. The stub classes in `repositories/database/`
  are ready — just needs the ORM implementation
- [ ] **PostgreSQL Support** — Extend the database backend to support
  PostgreSQL for production deployments
- [ ] **Redis Caching** — Cache frequently-read data (assignment lists,
  enrolled students) using Redis to reduce database load

### Notifications
- [ ] 🤝 **Email Notifications** — Integrate SendGrid or SMTP to send real
  email alerts for deadlines, submission confirmations, and grade releases.
  The `NotificationService` singleton is already wired — just needs an
  email delivery adapter
- [ ] **WebSocket Notifications** — Push real-time notifications to
  connected clients using FastAPI WebSockets

### API Enhancements
- [ ] 🤝 **Pagination** — Add `?page=` and `?limit=` query parameters to
  all list endpoints (`GET /api/assignments`, `GET /api/submissions`, etc.)
- [ ] **Filtering and Search** — Add `?status=`, `?course_id=`, `?due_before=`
  query parameters to assignment endpoints
- [ ] **Bulk Operations** — `POST /api/assignments/bulk-publish` to publish
  multiple assignments in one request

---

## 🌐 Long Term

### Frontend
- [ ] **React Dashboard** — Student-facing dashboard showing deadlines,
  submission status, and grades across all enrolled courses
- [ ] **Lecturer Portal** — Assignment management interface with submission
  grading workflow
- [ ] **Mobile App** — React Native app with push notifications for
  deadline reminders

### Infrastructure
- [ ] **Docker Support** — `Dockerfile` and `docker-compose.yml` for
  containerised local development and deployment
- [ ] **GitHub Pages Deployment** — Auto-deploy API documentation to
  GitHub Pages on every merge to `main`
- [ ] **OpenTelemetry Tracing** — Add distributed tracing for performance
  monitoring in production

### Integrations
- [ ] **LMS Integration** — Webhook support to sync assignments with
  external Learning Management Systems (Moodle, Canvas)
- [ ] **GitHub Classroom Integration** — Auto-create assignments from
  GitHub Classroom repositories

---

## 🤝 Good First Issues

These are ideal starting points for new contributors:

| Issue | Complexity | Label |
|-------|-----------|-------|
| Add CourseService and course endpoints | Low | `good-first-issue` |
| Add enrollment API endpoint | Low | `good-first-issue` |
| Increase test coverage on lecturer.py | Low | `good-first-issue` |
| Add pagination to list endpoints | Medium | `good-first-issue` |
| Add JWT authentication middleware | Medium | `good-first-issue` |

See the [Issues tab](https://github.com/219181527/student-assignment-tracker/issues)
for the full list with `good-first-issue` labels.

---

## 💡 Suggesting New Features

Have an idea not listed here? Open a
[GitHub Issue](https://github.com/219181527/student-assignment-tracker/issues/new)
with the label `feature-request` and describe:

1. What problem does it solve?
2. How would it work?
3. Are you willing to implement it?

---

## 📅 Release Schedule

| Version | Target | Focus |
|---------|--------|-------|
| v1.0.x | Released | Core API, service layer, CI/CD |
| v1.1.0 | Next | JWT auth, CourseService, enrollment endpoints |
| v1.2.0 | TBD | Database backend, email notifications |
| v2.0.0 | TBD | Frontend dashboard, Docker support |