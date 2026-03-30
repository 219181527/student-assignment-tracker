# Test Cases – Student Assignment Tracker

---

## 1. Functional Test Cases

| Test Case ID | Requirement ID | Description           | Steps                            | Expected Result              | Actual Result | Status |
| ------------ | -------------- | --------------------- | -------------------------------- | ---------------------------- | ------------- | ------ |
| TC-001       | FR1            | User registration     | 1. Enter valid details 2. Submit | Account created successfully | TBD           | TBD    |
| TC-002       | FR2            | User login            | 1. Enter credentials 2. Login    | Access granted               | TBD           | TBD    |
| TC-003       | FR3            | Create assignment     | 1. Enter details 2. Save         | Assignment stored            | TBD           | TBD    |
| TC-004       | FR4            | View assignments      | 1. Click view assignments        | Assignments displayed        | TBD           | TBD    |
| TC-005       | FR5            | Update assignment     | 1. Edit assignment 2. Save       | Assignment updated           | TBD           | TBD    |
| TC-006       | FR6            | Delete assignment     | 1. Select assignment 2. Delete   | Assignment removed           | TBD           | TBD    |
| TC-007       | FR7            | Track deadlines       | 1. Open dashboard                | Deadlines displayed          | TBD           | TBD    |
| TC-008       | FR9            | Receive notifications | 1. Wait for deadline alert       | Notification received        | TBD           | TBD    |

---

## 2. Non-Functional Test Scenarios

### Performance Test

**Test Case ID:** NFR-TC-001
**Description:** System performance under load

**Steps:**

1. Simulate 1,000 concurrent users
2. Perform assignment viewing

**Expected Result:**

* System responds within 2 seconds

---

### Security Test

**Test Case ID:** NFR-TC-002
**Description:** Authentication security

**Steps:**

1. Attempt login with invalid credentials
2. Attempt multiple failed logins

**Expected Result:**

* Access denied
* System prevents unauthorized access
