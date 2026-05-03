"""
lecturer.py — Lecturer class for Student Assignment Tracker
Extends User. Implements Lecturer entity from Class Diagram (Assignment 9).
"""

from typing import List
from src.user import User


class Lecturer(User):
    """
    Represents an instructor who creates and manages assignments.
    Inherits authentication and profile management from User.
    """

    def __init__(self, user_id: str, name: str, email: str, password: str,
                 department: str, employee_number: str):
        super().__init__(user_id, name, email, password, role="LECTURER")
        self._department = department
        self._employee_number = employee_number
        self._assignments: List = []  # List[Assignment]

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def create_assignment(self, course, title: str, description: str,
                          due_date, total_marks: int) -> "Assignment":
        """Create a new assignment and associate it with a course."""
        from src.assignment import Assignment
        assignment = Assignment(
            assignment_id=f"asgn_{len(self._assignments) + 1}_{course.course_id}",
            title=title,
            description=description,
            due_date=due_date,
            total_marks=total_marks,
            lecturer=self,
            course=course
        )
        self._assignments.append(assignment)
        course.add_assignment(assignment)
        return assignment

    def update_assignment(self, assignment, title: str = None, due_date=None) -> "Assignment":
        """Update an existing assignment's mutable fields."""
        if assignment not in self._assignments:
            raise PermissionError("Lecturer can only update their own assignments.")
        if title:
            assignment.title = title
        if due_date:
            assignment.due_date = due_date
        return assignment

    def delete_assignment(self, assignment) -> bool:
        """Remove an assignment created by this lecturer."""
        if assignment not in self._assignments:
            raise PermissionError("Lecturer can only delete their own assignments.")
        self._assignments.remove(assignment)
        return True

    def view_submissions(self, assignment) -> List:
        """Return all submissions for a given assignment."""
        if assignment not in self._assignments:
            raise PermissionError("Lecturer can only view submissions for their own assignments.")
        return assignment.get_submissions()

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    @property
    def department(self) -> str:
        return self._department

    @property
    def employee_number(self) -> str:
        return self._employee_number

    @property
    def assignments(self) -> List:
        return list(self._assignments)