"""
grade.py — Grade class for Student Assignment Tracker
Implements Grade entity from Class Diagram (Assignment 9).
"""

from datetime import date


class Grade:
    """
    Represents the assessed result of a Submission.
    Owned by Submission (composition). Zero or one per submission.
    """

    def __init__(self, grade_id: str, submission, score: float, feedback: str):
        if score < 0:
            raise ValueError("Score cannot be negative.")
        self._grade_id = grade_id
        self._submission = submission
        self._score = score
        self._feedback = feedback
        self._graded_date = date.today()
        # Register this grade on the submission
        submission.assign_grade(self)

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def assign_grade(self, score: float, feedback: str) -> None:
        """Update score and feedback (re-grading scenario)."""
        if score < 0:
            raise ValueError("Score cannot be negative.")
        self._score = score
        self._feedback = feedback
        self._graded_date = date.today()

    def get_percentage(self, total_marks: int) -> float:
        """Calculate percentage score relative to total marks."""
        if total_marks <= 0:
            raise ValueError("Total marks must be greater than zero.")
        return round((self._score / total_marks) * 100, 2)

    # ------------------------------------------------------------------ #
    # Getters
    # ------------------------------------------------------------------ #

    @property
    def grade_id(self) -> str:
        return self._grade_id

    @property
    def score(self) -> float:
        return self._score

    @property
    def feedback(self) -> str:
        return self._feedback

    @property
    def graded_date(self) -> date:
        return self._graded_date

    def __repr__(self) -> str:
        return f"Grade(id={self._grade_id}, score={self._score}, date={self._graded_date})"