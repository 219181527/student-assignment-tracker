"""
api/routes/assignments.py — Assignment API Routes
Student Assignment Tracker

Endpoints:
    POST   /api/assignments                         Create a new assignment
    GET    /api/assignments                         List all assignments
    GET    /api/assignments/{id}                    Get assignment by ID
    PUT    /api/assignments/{id}                    Update an assignment
    DELETE /api/assignments/{id}                    Delete a draft assignment
    POST   /api/assignments/{id}/publish            Publish an assignment
    POST   /api/assignments/{id}/close              Close an assignment
    GET    /api/assignments/course/{course_id}      Get assignments for a course
    GET    /api/assignments/lecturer/{lecturer_id}  Get assignments for a lecturer
    GET    /api/assignments/overdue                 Get overdue assignments
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from api.schemas import (
    CreateAssignmentRequest, UpdateAssignmentRequest,
    AssignmentActionRequest, AssignmentResponse,
    MessageResponse, ErrorResponse,
)
from api.dependencies import get_factory
from services.assignment_service import AssignmentService
from services.base import (
    NotFoundError, ValidationError, ConflictError, PermissionError
)
from repositories.factory import RepositoryFactory

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])


def _assignment_service(
    factory: RepositoryFactory = Depends(get_factory),
) -> AssignmentService:
    return AssignmentService(factory)


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new assignment",
    responses={
        404: {"model": ErrorResponse, "description": "Lecturer or course not found"},
        409: {"model": ErrorResponse, "description": "Course is inactive"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def create_assignment(
    body: CreateAssignmentRequest,
    svc: AssignmentService = Depends(_assignment_service),
):
    """
    Create a new assignment in DRAFT status.
    Lecturer and course must exist. Due date must be today or in the future.
    """
    try:
        assignment = svc.create_assignment(
            body.lecturer_id, body.course_id, body.title,
            body.description, body.due_date, body.total_marks,
        )
        return AssignmentResponse.from_domain(assignment)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.get(
    "",
    response_model=List[AssignmentResponse],
    summary="List all assignments",
)
def list_assignments(svc: AssignmentService = Depends(_assignment_service)):
    """Return all assignments across all courses."""
    return [AssignmentResponse.from_domain(a) for a in svc.get_all_assignments()]


@router.get(
    "/overdue",
    response_model=List[AssignmentResponse],
    summary="List overdue assignments",
)
def list_overdue(svc: AssignmentService = Depends(_assignment_service)):
    """Return all published assignments whose due date has passed."""
    return [AssignmentResponse.from_domain(a) for a in svc.get_overdue_assignments()]


@router.get(
    "/course/{course_id}",
    response_model=List[AssignmentResponse],
    summary="List assignments for a course",
    responses={404: {"model": ErrorResponse}},
)
def list_by_course(
    course_id: str,
    svc: AssignmentService = Depends(_assignment_service),
):
    """Return all assignments belonging to a given course."""
    try:
        return [
            AssignmentResponse.from_domain(a)
            for a in svc.get_assignments_for_course(course_id)
        ]
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get(
    "/lecturer/{lecturer_id}",
    response_model=List[AssignmentResponse],
    summary="List assignments created by a lecturer",
    responses={404: {"model": ErrorResponse}},
)
def list_by_lecturer(
    lecturer_id: str,
    svc: AssignmentService = Depends(_assignment_service),
):
    """Return all assignments created by a specific lecturer."""
    try:
        return [
            AssignmentResponse.from_domain(a)
            for a in svc.get_assignments_for_lecturer(lecturer_id)
        ]
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get(
    "/{assignment_id}",
    response_model=AssignmentResponse,
    summary="Get an assignment by ID",
    responses={404: {"model": ErrorResponse}},
)
def get_assignment(
    assignment_id: str,
    svc: AssignmentService = Depends(_assignment_service),
):
    """Retrieve a single assignment by its unique ID."""
    try:
        return AssignmentResponse.from_domain(svc.get_assignment(assignment_id))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put(
    "/{assignment_id}",
    response_model=AssignmentResponse,
    summary="Update an assignment",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse, "description": "Lecturer does not own the assignment"},
        409: {"model": ErrorResponse, "description": "Cannot update a CLOSED assignment"},
    },
)
def update_assignment(
    assignment_id: str,
    body: UpdateAssignmentRequest,
    svc: AssignmentService = Depends(_assignment_service),
):
    """Update an assignment's title or due date. Only the creating lecturer can update."""
    try:
        updated = svc.update_assignment(
            assignment_id, body.lecturer_id, body.title, body.due_date
        )
        return AssignmentResponse.from_domain(updated)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.delete(
    "/{assignment_id}",
    response_model=MessageResponse,
    summary="Delete a draft assignment",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse, "description": "Only DRAFT assignments can be deleted"},
    },
)
def delete_assignment(
    assignment_id: str,
    lecturer_id: str,
    svc: AssignmentService = Depends(_assignment_service),
):
    """Delete an assignment. Only DRAFT assignments can be deleted. Pass lecturer_id as a query parameter."""
    try:
        svc.delete_assignment(assignment_id, lecturer_id)
        return MessageResponse(message=f"Assignment '{assignment_id}' deleted.")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)


# ---------------------------------------------------------------------------
# Lifecycle actions
# ---------------------------------------------------------------------------

@router.post(
    "/{assignment_id}/publish",
    response_model=AssignmentResponse,
    summary="Publish an assignment",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse, "description": "Assignment is not in DRAFT status"},
    },
)
def publish_assignment(
    assignment_id: str,
    body: AssignmentActionRequest,
    svc: AssignmentService = Depends(_assignment_service),
):
    """
    Transition an assignment from DRAFT to PUBLISHED.
    Notifies all enrolled students. Only the creating lecturer can publish.
    """
    try:
        published = svc.publish_assignment(assignment_id, body.lecturer_id)
        return AssignmentResponse.from_domain(published)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.post(
    "/{assignment_id}/close",
    response_model=AssignmentResponse,
    summary="Close an assignment",
    responses={
        404: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse, "description": "Assignment is not PUBLISHED"},
    },
)
def close_assignment(
    assignment_id: str,
    body: AssignmentActionRequest,
    svc: AssignmentService = Depends(_assignment_service),
):
    """
    Transition an assignment from PUBLISHED to CLOSED.
    No further submissions will be accepted. Only the creating lecturer can close.
    """
    try:
        closed = svc.close_assignment(assignment_id, body.lecturer_id)
        return AssignmentResponse.from_domain(closed)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)