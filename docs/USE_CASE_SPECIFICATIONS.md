# Use Case Specifications – Student Assignment Tracker

---

## Use Case 1: User Registration

**Actor:** Student / Lecturer
**Description:** Allows a user to create an account.

**Preconditions:**

* User is not registered

**Postconditions:**

* User account is created successfully

**Basic Flow:**

1. User enters email and password
2. System validates input
3. System creates account
4. Confirmation is displayed

**Alternative Flow:**

* Invalid input → System displays error message

---

## Use Case 2: User Login

**Actor:** Student / Lecturer

**Preconditions:**

* User has a registered account

**Postconditions:**

* User is logged into the system

**Basic Flow:**

1. User enters credentials
2. System validates credentials
3. User is granted access

**Alternative Flow:**

* Invalid credentials → Access denied

---

## Use Case 3: Create Assignment

**Actor:** Lecturer

**Preconditions:**

* Lecturer is logged in

**Postconditions:**

* Assignment is stored in system

**Basic Flow:**

1. Lecturer enters assignment details
2. System validates input
3. System saves assignment

**Alternative Flow:**

* Missing fields → System prompts for completion

---

## Use Case 4: View Assignments

**Actor:** Student

**Preconditions:**

* Student is logged in

**Postconditions:**

* Assignments are displayed

**Basic Flow:**

1. Student selects "View Assignments"
2. System retrieves data
3. Assignments are displayed

**Alternative Flow:**

* No assignments → Display message

---

## Use Case 5: Update Assignment

**Actor:** Lecturer

**Preconditions:**

* Assignment exists

**Postconditions:**

* Assignment is updated

**Basic Flow:**

1. Lecturer selects assignment
2. Updates details
3. System saves changes

**Alternative Flow:**

* Invalid update → System rejects changes

---

## Use Case 6: Delete Assignment

**Actor:** Lecturer

**Preconditions:**

* Assignment exists

**Postconditions:**

* Assignment is removed

**Basic Flow:**

1. Lecturer selects assignment
2. Confirms deletion
3. System deletes assignment

**Alternative Flow:**

* Cancellation → No action taken

---

## Use Case 7: Track Deadlines

**Actor:** Student

**Preconditions:**

* Assignments exist

**Postconditions:**

* Deadlines are displayed

**Basic Flow:**

1. Student views dashboard
2. System displays deadlines

**Alternative Flow:**

* No deadlines → Inform user

---

## Use Case 8: Receive Notifications

**Actor:** Student

**Preconditions:**

* User has upcoming assignments

**Postconditions:**

* Notification is delivered

**Basic Flow:**

1. System checks deadlines
2. System sends notification

**Alternative Flow:**

* Notification failure → Retry or log error
