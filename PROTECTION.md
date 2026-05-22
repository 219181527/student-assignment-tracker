# 🔒 Branch Protection Rules
## Student Assignment Tracker

---

## Overview

Branch protection rules are enforced on the `main` branch to ensure that
no untested, unreviewed, or broken code ever reaches production. Every
change to `main` must pass through a pull request, pass all automated
tests, and receive at least one peer review before merging.

---

## Rules Configured on `main`

| Rule | Setting | Reason |
|------|---------|--------|
| Require pull request before merging | ✅ Enabled | No direct pushes to `main` — all changes go through a PR |
| Required approving reviews | 1 minimum | A second pair of eyes catches logic errors and enforces standards |
| Dismiss stale reviews on new push | ✅ Enabled | A new commit invalidates previous approval — must re-review |
| Require status checks to pass | ✅ Enabled | CI pipeline must be green before merge is allowed |
| Require branches to be up to date | ✅ Enabled | PR branch must include latest `main` before merging |
| Do not allow bypassing the above rules | ✅ Enabled | Rules apply to administrators too — no exceptions |
| Restrict direct pushes | ✅ Enabled | Even repo owners cannot push directly to `main` |

---

## Why Each Rule Matters

### 1. Require Pull Request Before Merging

Direct pushes to `main` bypass all quality gates. A PR creates a
structured review process where changes are visible, discussable, and
traceable. Every line that reaches `main` has an associated PR with
context, reviewers, and linked issues.

**Without this rule:** A developer could push broken code directly to
`main` at 2am and silently break the production API for all users.

---

### 2. Required Approving Reviews (minimum 1)

Peer review catches bugs that automated tests miss — logic errors,
misunderstood requirements, security issues, and code that works but
violates architectural principles.

**Without this rule:** A developer could approve their own PR by merging
immediately after opening it. Self-review catches nothing.

---

### 3. Dismiss Stale Reviews on New Push

If a reviewer approves a PR and then the author pushes five more commits,
the original approval no longer reflects the current state of the code.
Stale review dismissal forces re-review after any new push.

**Without this rule:** A PR could be approved in a clean state and then
have breaking changes pushed afterwards — still appearing as "approved."

---

### 4. Require Status Checks to Pass (CI Pipeline)

The CI workflow runs the full test suite (265 tests) on every push. If any
test fails, the merge button is blocked. This guarantees that `main` is
always in a passing state.

**Without this rule:** A developer could merge a PR where tests are failing
or skipped, introducing regressions that affect all downstream work.

---

### 5. Require Branches to Be Up to Date

A PR branch must include the latest commits from `main` before merging.
This prevents integration conflicts from being hidden — the CI runs against
the actual merged state, not just the feature branch in isolation.

**Without this rule:** Two PRs could both pass CI independently but
conflict with each other when merged sequentially, breaking `main`.

---

### 6. Do Not Allow Bypassing Rules (applies to admins)

Rules that admins can bypass are not real rules — they create a culture
of exceptions. Applying protection to all users, including repository
owners, ensures the process is followed consistently.

**Without this rule:** Pressure situations (tight deadlines, "just this
once") lead to shortcuts that accumulate technical debt and erode trust
in the codebase.

---

## Branch Strategy

```
main          ← Protected. Production-ready only. Never pushed to directly.
  └── dev     ← Integration branch. PRs merged here first.
        └── feature/xxx  ← Short-lived feature branches per task.
```

All development happens on feature branches. Feature branches are merged
into `dev` via PR. When `dev` is stable and all tests pass, a PR from
`dev` → `main` is raised, reviewed, and merged — triggering the CD
pipeline which generates a release artifact.

---

## Relationship to CI/CD

Branch protection and CI/CD are complementary:

```
Developer pushes to feature branch
        ↓
CI runs automatically (test suite, linting)
        ↓
PR opened → peer review required
        ↓
Status checks must pass (CI green)
        ↓
Merge to main approved
        ↓
CD pipeline runs → release artifact generated
```

Without branch protection, the CD pipeline could be triggered by broken
code. Without CI, the status check requirement would have nothing to
verify. Together they form a complete quality gate.

---

## Screenshot

See `screenshots/branch_protection.png` for the configured rules as
shown in GitHub's repository settings.