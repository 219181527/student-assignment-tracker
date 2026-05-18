"""
api/routes/submissions.py — Submission API Routes
Student Assignment Tracker

Endpoints:
    POST   /api/submissions                              Submit an assignment
    GET    /api/submissions/{id}                         Get submission by ID
    GET    /api/submissions/assignment/{assignment_id}   Get all submissions for an assignment
    GET    /api/submissions/student/{student_id}         Get all submissions by a student
    POST   /api/submissions/{id}/grade                   Grade a submission
    GET    /api/submissions/{id}/grade                   Get the grade for a submission
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional

from api.schemas import (
    SubmitAssignmentRequest, GradeSubmissionRequest,
    SubmissionResponse, GradeResponse, ErrorResponse,
)
from api.dependencies import get_factory
from services.submission_service import SubmissionService
from services.base import (
    NotFoundError, ValidationError, ConflictError, PermissionError
)
from repositories.factory import RepositoryFactory

router = APIRouter(prefix="/api/submissions", tags=["Submissions"])


def _submission_service(
    factory: RepositoryFactory = Depends(get_factory),
) -> SubmissionService:
    return SubmissionService(factory)


# ---------------------------------------------------------------------------
# Submission endpoints
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit an assignment",
    responses={
        404: {"model": ErrorResponse, "description": "Student or assignment not found"},
        403: {"model": ErrorResponse, "description": "Student not enrolled in the course"},
        409: {"model": ErrorResponse, "description": "Student has already submitted"},
        422: {"model": ErrorResponse, "description": "Assignment is not PUBLISHED"},
    },
)
def submit_assignment(
    body: SubmitAssignmentRequest,
    assignment_id: str,
    svc: SubmissionService = Depends(_submission_service),
):
    """
    Submit an assignment on behalf of a student.

    - Assignment must be PUBLISHED
    - Student must be actively enrolled in the course
    - One submission per student per assignment
    """
    try:
        submission = svc.submit_assignment(
            body.student_id, assignment_id, body.file_url
        )
        return SubmissionResponse.from_domain(submission)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.get(
    "/assignment/{assignment_id}",
    response_model=List[SubmissionResponse],
    summary="List submissions for an assignment",
    responses={404: {"model": ErrorResponse}},
)
def list_by_assignment(
    assignment_id: str,
    svc: SubmissionService = Depends(_submission_service),
):
    """Return all submissions for a given assignment."""
    try:
        return [
            SubmissionResponse.from_domain(s)
            for s in svc.get_submissions_for_assignment(assignment_id)
        ]
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get(
    "/student/{student_id}",
    response_model=List[SubmissionResponse],
    summary="List submissions by a student",
    responses={404: {"model": ErrorResponse}},
)
def list_by_student(
    student_id: str,
    svc: SubmissionService = Depends(_submission_service),
):
    """Return all submissions made by a given student."""
    try:
        return [
            SubmissionResponse.from_domain(s)
            for s in svc.get_submissions_for_student(student_id)
        ]
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get(
    "/{submission_id}",
    response_model=SubmissionResponse,
    summary="Get a submission by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_submission(
    submission_id: str,
    svc: SubmissionService = Depends(_submission_service),
):
    """Retrieve a single submission by its unique ID."""
    try:
        return SubmissionResponse.from_domain(svc.get_submission(submission_id))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


# ---------------------------------------------------------------------------
# Grading endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/{submission_id}/grade",
    response_model=GradeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Grade a submission",
    responses={
        404: {"model": ErrorResponse, "description": "Submission not found"},
        403: {"model": ErrorResponse, "description": "Lecturer does not own the assignment"},
        409: {"model": ErrorResponse, "description": "Submission already graded"},
        422: {"model": ErrorResponse, "description": "Score out of range"},
    },
)
def grade_submission(
    submission_id: str,
    body: GradeSubmissionRequest,
    svc: SubmissionService = Depends(_submission_service),
):
    """
    Assign a grade to a submission.

    - Only the creating lecturer can grade it
    - Score must be between 0 and the assignment's total marks
    - A submission can only be graded once
    """
    try:
        submission = svc.get_submission(submission_id)
        grade = svc.grade_submission(
            submission_id, body.lecturer_id, body.score, body.feedback
        )
        return GradeResponse.from_domain(
            grade, total_marks=submission.assignment.total_marks
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.get(
    "/{submission_id}/grade",
    response_model=Optional[GradeResponse],
    summary="Get the grade for a submission",
    responses={404: {"model": ErrorResponse}},
)
def get_grade(
    submission_id: str,
    svc: SubmissionService = Depends(_submission_service),
):
    """
    Return the grade for a submission.
    Returns null if the submission has not yet been graded.
    """
    try:
        submission = svc.get_submission(submission_id)
        grade = svc.get_grade_for_submission(submission_id)
        if not grade:
            return None
        return GradeResponse.from_domain(
            grade, total_marks=submission.assignment.total_marks
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)