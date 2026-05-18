"""
services/submission_service.py — Submission Service
Student Assignment Tracker

Encapsulates all business logic for assignment submissions and grading:
- Submission with enrollment and assignment-status validation
- Grading with score range enforcement
- Submission status tracking per student

Business rules enforced:
- Students can only submit to PUBLISHED assignments
- Students must be actively enrolled in the assignment's course
- One submission per student per assignment
- Score cannot exceed assignment's total marks
- Score cannot be negative
- Only SUBMITTED or LATE submissions can be graded
"""

from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from services.base import (
    BaseService, NotFoundError, ValidationError,
    ConflictError, PermissionError,
)

if TYPE_CHECKING:
    from repositories.factory.repository_factory import RepositoryFactory
    from src.submission import Submission
    from src.grade import Grade


class SubmissionService(BaseService):
    """
    Service class for assignment submission and grading workflows.

    Depends on:
        SubmissionRepository  — persist/retrieve submissions
        AssignmentRepository  — validate assignment state
        StudentRepository     — validate student enrollment
        GradeRepository       — persist/retrieve grades
        EnrollmentRepository  — check active enrollment
    """

    def __init__(self, repository_factory: "RepositoryFactory"):
        self._factory = repository_factory
        self._submission_repo = repository_factory.get_submission_repository()
        self._assignment_repo = repository_factory.get_assignment_repository()
        self._student_repo = repository_factory.get_student_repository()
        self._grade_repo = repository_factory.get_grade_repository()
        self._enrollment_repo = repository_factory.get_enrollment_repository()

    # ------------------------------------------------------------------ #
    # Submission
    # ------------------------------------------------------------------ #

    def submit_assignment(
        self,
        student_id: str,
        assignment_id: str,
        file_url: str,
    ) -> "Submission":
        """
        Submit an assignment on behalf of a student.

        Business rules:
        - Student must exist
        - Assignment must exist and be PUBLISHED
        - Student must be actively enrolled in the assignment's course
        - Student cannot submit the same assignment twice

        Args:
            student_id:    ID of the submitting student
            assignment_id: ID of the target assignment
            file_url:      URL of the submitted file

        Returns:
            The newly created Submission instance.

        Raises:
            NotFoundError:  If student or assignment doesn't exist.
            ValidationError: If assignment is not PUBLISHED.
            PermissionError: If student is not enrolled in the course.
            ConflictError:   If student has already submitted.
        """
        self._require(student_id, "student_id")
        self._require(assignment_id, "assignment_id")
        self._require(file_url, "file_url")

        student = self._student_repo.find_by_id(student_id)
        if not student:
            raise NotFoundError("Student", student_id)

        assignment = self._assignment_repo.find_by_id(assignment_id)
        if not assignment:
            raise NotFoundError("Assignment", assignment_id)

        # Business rule: assignment must be PUBLISHED
        if assignment.status != "PUBLISHED":
            raise ValidationError(
                f"Assignment is '{assignment.status}' — "
                f"submissions are only accepted for PUBLISHED assignments."
            )

        # Business rule: student must be actively enrolled in the course
        course_id = assignment.course.course_id
        enrollment = self._enrollment_repo.find_by_student_and_course(
            student_id, course_id
        )
        if not enrollment or enrollment.status != "ACTIVE":
            raise PermissionError(
                f"Student '{student_id}' is not actively enrolled in "
                f"course '{course_id}'."
            )

        # Business rule: one submission per student per assignment
        existing = self._submission_repo.find_by_student_and_assignment(
            student_id, assignment_id
        )
        if existing:
            raise ConflictError(
                f"Student '{student_id}' has already submitted "
                f"assignment '{assignment_id}'."
            )

        submission = student.submit_assignment(assignment, file_url)
        self._submission_repo.save(submission)
        return submission

    # ------------------------------------------------------------------ #
    # Grading
    # ------------------------------------------------------------------ #

    def grade_submission(
        self,
        submission_id: str,
        lecturer_id: str,
        score: float,
        feedback: str,
    ) -> "Grade":
        """
        Assign a grade to a submission.

        Business rules:
        - Submission must exist
        - Submission must be in SUBMITTED or LATE status (not already graded)
        - Score must be between 0 and the assignment's total_marks (inclusive)
        - Only the assignment's creating lecturer can grade it

        Args:
            submission_id: ID of the submission to grade
            lecturer_id:   ID of the grading lecturer
            score:         Numeric mark awarded
            feedback:      Qualitative comments

        Returns:
            The newly created Grade instance.

        Raises:
            NotFoundError:   If submission doesn't exist.
            ConflictError:   If submission is already graded.
            ValidationError: If score is out of range.
            PermissionError: If lecturer doesn't own the assignment.
        """
        self._require(submission_id, "submission_id")
        self._require(lecturer_id, "lecturer_id")
        self._require(feedback, "feedback")
        self._require_not_none(score, "score")

        submission = self._submission_repo.find_by_id(submission_id)
        if not submission:
            raise NotFoundError("Submission", submission_id)

        # Business rule: cannot re-grade
        if submission.status == "GRADED":
            raise ConflictError(
                f"Submission '{submission_id}' has already been graded."
            )

        # Business rule: lecturer must own the assignment
        assignment = submission.assignment
        if assignment._lecturer.user_id != lecturer_id:
            raise PermissionError(
                f"Lecturer '{lecturer_id}' does not own assignment "
                f"'{assignment.assignment_id}'."
            )

        # Business rule: score range validation
        if score < 0:
            raise ValidationError("Score cannot be negative.")
        if score > assignment.total_marks:
            raise ValidationError(
                f"Score {score} exceeds total marks ({assignment.total_marks}) "
                f"for this assignment."
            )

        from src.grade import Grade
        grade_id = f"grade_{submission_id}"
        grade = Grade(grade_id, submission, score, feedback)
        self._grade_repo.save(grade)
        self._submission_repo.save(submission)  # Update status to GRADED
        return grade

    # ------------------------------------------------------------------ #
    # Retrieval
    # ------------------------------------------------------------------ #

    def get_submission(self, submission_id: str) -> "Submission":
        """Retrieve a submission by ID. Raises NotFoundError if missing."""
        self._require(submission_id, "submission_id")
        submission = self._submission_repo.find_by_id(submission_id)
        if not submission:
            raise NotFoundError("Submission", submission_id)
        return submission

    def get_submissions_for_assignment(
        self, assignment_id: str
    ) -> List["Submission"]:
        """Return all submissions for a given assignment."""
        self._require(assignment_id, "assignment_id")
        assignment = self._assignment_repo.find_by_id(assignment_id)
        if not assignment:
            raise NotFoundError("Assignment", assignment_id)
        return self._submission_repo.find_by_assignment(assignment_id)

    def get_submissions_for_student(
        self, student_id: str
    ) -> List["Submission"]:
        """Return all submissions made by a given student."""
        self._require(student_id, "student_id")
        student = self._student_repo.find_by_id(student_id)
        if not student:
            raise NotFoundError("Student", student_id)
        return self._submission_repo.find_by_student(student_id)

    def get_grade_for_submission(
        self, submission_id: str
    ) -> Optional["Grade"]:
        """
        Return the grade for a submission, or None if not yet graded.

        Raises:
            NotFoundError: If the submission doesn't exist.
        """
        self._require(submission_id, "submission_id")
        submission = self._submission_repo.find_by_id(submission_id)
        if not submission:
            raise NotFoundError("Submission", submission_id)
        return self._grade_repo.find_by_submission(submission_id)

    def get_student_grade_for_assignment(
        self, student_id: str, assignment_id: str
    ) -> Optional["Grade"]:
        """
        Return the grade a student received for a specific assignment.
        Returns None if the student hasn't submitted or isn't yet graded.
        """
        self._require(student_id, "student_id")
        self._require(assignment_id, "assignment_id")

        submission = self._submission_repo.find_by_student_and_assignment(
            student_id, assignment_id
        )
        if not submission:
            return None
        return self._grade_repo.find_by_submission(submission.submission_id)