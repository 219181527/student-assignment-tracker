"""
api/routes/users.py — User API Routes
Student Assignment Tracker

Endpoints:
    POST   /api/users/students          Register a new student
    POST   /api/users/lecturers         Register a new lecturer
    POST   /api/users/login             Authenticate a user
    GET    /api/users/students          List all students
    GET    /api/users/students/{id}     Get a student by ID
    PUT    /api/users/students/{id}     Update a student's profile
    GET    /api/users/lecturers         List all lecturers
    GET    /api/users/lecturers/{id}    Get a lecturer by ID
    PUT    /api/users/lecturers/{id}    Update a lecturer's profile
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from api.schemas import (
    StudentRegisterRequest, LecturerRegisterRequest, LoginRequest,
    UpdateProfileRequest, StudentResponse, LecturerResponse,
    LoginResponse, MessageResponse, ErrorResponse,
)
from api.dependencies import get_factory
from services.user_service import UserService
from services.base import NotFoundError, ValidationError, ConflictError
from repositories.factory import RepositoryFactory

router = APIRouter(prefix="/api/users", tags=["Users"])


def _user_service(factory: RepositoryFactory = Depends(get_factory)) -> UserService:
    return UserService(factory)


# ---------------------------------------------------------------------------
# Student endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student",
    responses={
        409: {"model": ErrorResponse, "description": "Email or student number already registered"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def register_student(
    body: StudentRegisterRequest,
    svc: UserService = Depends(_user_service),
):
    """Register a new student account. Email and student number must be unique."""
    try:
        student = svc.register_student(
            body.user_id, body.name, body.email, body.password,
            body.student_number, body.year_of_study,
        )
        return StudentResponse.from_domain(student)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.get(
    "/students",
    response_model=List[StudentResponse],
    summary="List all students",
)
def list_students(svc: UserService = Depends(_user_service)):
    """Return all registered students."""
    return [StudentResponse.from_domain(s) for s in svc.get_all_students()]


@router.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    summary="Get a student by ID",
    responses={404: {"model": ErrorResponse, "description": "Student not found"}},
)
def get_student(student_id: str, svc: UserService = Depends(_user_service)):
    """Retrieve a student by their unique ID."""
    try:
        return StudentResponse.from_domain(svc.get_student(student_id))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put(
    "/students/{student_id}",
    response_model=StudentResponse,
    summary="Update a student's profile",
    responses={
        404: {"model": ErrorResponse, "description": "Student not found"},
        409: {"model": ErrorResponse, "description": "Email already in use"},
    },
)
def update_student(
    student_id: str,
    body: UpdateProfileRequest,
    svc: UserService = Depends(_user_service),
):
    """Update a student's name or email address."""
    try:
        updated = svc.update_profile(student_id, "STUDENT", body.name, body.email)
        return StudentResponse.from_domain(updated)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)


# ---------------------------------------------------------------------------
# Lecturer endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/lecturers",
    response_model=LecturerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new lecturer",
    responses={
        409: {"model": ErrorResponse, "description": "Email or employee number already registered"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def register_lecturer(
    body: LecturerRegisterRequest,
    svc: UserService = Depends(_user_service),
):
    """Register a new lecturer account. Employee number must be unique."""
    try:
        lecturer = svc.register_lecturer(
            body.user_id, body.name, body.email, body.password,
            body.department, body.employee_number,
        )
        return LecturerResponse.from_domain(lecturer)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.get(
    "/lecturers",
    response_model=List[LecturerResponse],
    summary="List all lecturers",
)
def list_lecturers(svc: UserService = Depends(_user_service)):
    """Return all registered lecturers."""
    return [LecturerResponse.from_domain(l) for l in svc.get_all_lecturers()]


@router.get(
    "/lecturers/{lecturer_id}",
    response_model=LecturerResponse,
    summary="Get a lecturer by ID",
    responses={404: {"model": ErrorResponse, "description": "Lecturer not found"}},
)
def get_lecturer(lecturer_id: str, svc: UserService = Depends(_user_service)):
    """Retrieve a lecturer by their unique ID."""
    try:
        return LecturerResponse.from_domain(svc.get_lecturer(lecturer_id))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put(
    "/lecturers/{lecturer_id}",
    response_model=LecturerResponse,
    summary="Update a lecturer's profile",
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
def update_lecturer(
    lecturer_id: str,
    body: UpdateProfileRequest,
    svc: UserService = Depends(_user_service),
):
    """Update a lecturer's name or email address."""
    try:
        updated = svc.update_profile(lecturer_id, "LECTURER", body.name, body.email)
        return LecturerResponse.from_domain(updated)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=e.message)


# ---------------------------------------------------------------------------
# Auth endpoint
# ---------------------------------------------------------------------------

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Authenticate a user",
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        422: {"model": ErrorResponse, "description": "Invalid credentials or inactive account"},
    },
)
def login(body: LoginRequest, svc: UserService = Depends(_user_service)):
    """
    Authenticate a student or lecturer by email, password, and role.
    Returns user info on success.
    """
    try:
        user = svc.login(body.email, body.password, body.role)
        return LoginResponse(
            message="Login successful.",
            user_id=user.user_id,
            role=user.role,
            name=user.name,
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)