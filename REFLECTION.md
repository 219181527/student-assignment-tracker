# 🧠 Reflection — Open-Source Collaboration and Peer Review

## Assignment 14: Peer Review, Onboarding, and Open-Source Collaboration

---

## Introduction

Preparing the Student Assignment Tracker for open-source collaboration was
a qualitatively different challenge from anything in the previous assignments.
Building features, writing tests, and setting up CI/CD are largely
technical exercises with clear right and wrong answers. Preparing a repository
for strangers to contribute to requires a different kind of thinking — empathy
for someone who has never seen your code before, and the discipline to document
decisions that feel obvious to you but are completely opaque to everyone else.

---

## How I Improved the Repository Based on Peer Feedback

The peer review process revealed gaps that I had not noticed during development
because I was too close to the codebase. The most significant improvement was
the addition of `CONTRIBUTING.md`. During development, the setup process lived
entirely in my head — I knew to run `uvicorn api.main:app --reload` to start
the API, I knew that `pytest tests/ -v` ran the suite, and I knew that all
changes went through `dev` before `main`. None of that was written down in a
way that would help a new contributor.

Writing `CONTRIBUTING.md` forced me to walk through the setup process as if
I were a complete stranger to the project. In doing so, I discovered that
the project had no `requirements.txt` — dependencies were scattered across
`pip install` commands in the CI workflow. A new contributor would have had
no way to install the right packages without reading the GitHub Actions YAML
carefully. Creating `requirements.txt` fixed this for both contributors and
the CI pipeline simultaneously.

The `ROADMAP.md` was another meaningful addition. It transformed a collection
of GitHub issues into a coherent vision — contributors could see not just what
individual tasks needed doing, but how those tasks fit into a larger plan. The
distinction between short-term, medium-term, and long-term features gave
contributors a sense of the project's trajectory and helped them self-select
work that matched their skills and interests.

---

## Challenges in Onboarding Contributors

The most significant onboarding challenge was the absence of a `CourseService`
and enrollment endpoints in the API. New contributors looking at the Swagger
UI at `/docs` would see endpoints for users, assignments, and submissions —
but no way to create courses or enroll students. These operations had to be
done directly via the repository layer, which is not exposed through the API.
This created a confusing gap: the system's data model clearly includes courses
and enrollments as first-class entities, but the API treats them as
implementation details.

This gap was intentional during development — the focus was on the assignment
submission workflow — but from a contributor's perspective it looks like an
oversight. The `good-first-issue` label on the CourseService task directly
addressed this by giving contributors a clear, well-scoped entry point with
an established pattern to follow from `UserService` and `AssignmentService`.

A second challenge was the architecture's layered nature. The project follows
a strict separation: domain classes (`src/`) know nothing about services,
services know nothing about the API, and the API knows nothing about
repositories directly. For contributors who are new to layered architecture,
this can be disorienting — it's not immediately obvious why you cannot just
call the repository from a route handler. Documenting this explicitly in
`CONTRIBUTING.md` under "Architecture Rules" was essential for preventing
well-intentioned PRs that bypassed the service layer entirely.

---

## Lessons Learned About Open-Source Collaboration

The most important lesson was that **documentation is not a deliverable — it
is a product**. Throughout the earlier assignments, documentation was something
produced at the end of each task: write the code, then write about the code.
Preparing for open-source collaboration inverted this. The `CONTRIBUTING.md`,
`ROADMAP.md`, and issue descriptions needed to be written with the same care
as the source code itself, because they are what contributors interact with
first. A brilliant codebase with poor documentation is inaccessible; a
well-documented codebase with average code attracts contributors who can
improve it.

The second lesson was about **issue granularity**. The most actionable issues
were the ones with explicit acceptance criteria, references to specific files
and line numbers, and a clear statement of why the issue matters. Vague issues
like "improve performance" attract no one. Specific issues like "add
`?page=` and `?limit=` query parameters to the five list endpoints in
`api/routes/`" give contributors exactly what they need to get started without
requiring a conversation with the maintainer first.

The third lesson was about **reciprocity in open-source communities**. The 22
forks and 21 stars this repository received came through genuine mutual
engagement — I reviewed classmates' repositories, starred the ones I found
well-structured, and forked the ones I wanted to explore further. This mirrors
how real open-source communities work: visibility comes from contributing to
others, not just from building something good in isolation. The best open-source
projects are embedded in communities of practice where contributors move fluidly
between maintaining their own work and contributing to others'.

---

## Conclusion

Assignment 14 reframed the entire project from a personal codebase into a
public resource. The technical work was already done — what remained was making
it legible, welcoming, and useful to people who had no part in building it.
That process of externalising internal knowledge, documenting implicit
conventions, and creating structured entry points for new contributors is one
of the most transferable skills in software engineering. Whether contributing
to a company's internal platform, an industry open-source project, or an
academic collaboration, the ability to prepare a codebase for others to work
on is as valuable as the ability to build it in the first place.