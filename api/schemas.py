"""
api/schemas.py — Pydantic Request/Response Schemas
Student Assignment Tracker — Pydantic v2 compatible
"""

from __future__ import annotations
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class StudentRegisterRequest(BaseModel):
    user_id: str = Field(..., description="Unique student identifier")
    name: str = Field(..., description="Full display name")
    email: str = Field(..., description="Login email address")
    password: str = Field(..., min_length=6, description="Plain-text password")
    student_number: str = Field(..., description="Institutional student number")
    year_of_study: int = Field(..., ge=1, le=10, description="Current academic year")
    model_config = ConfigDict(json_schema_extra={"example": {
        "user_id": "s1", "name": "Alice Dlamini", "email": "alice@uni.ac.za",
        "password": "securepass", "student_number": "219181527", "year_of_study": 3,
    }})


class LecturerRegisterRequest(BaseModel):
    user_id: str = Field(..., description="Unique lecturer identifier")
    name: str = Field(..., description="Full display name")
    email: str = Field(..., description="Login email address")
    password: str = Field(..., min_length=6, description="Plain-text password")
    department: str = Field(..., description="Academic department")
    employee_number: str = Field(..., description="Institutional employee number")
    model_config = ConfigDict(json_schema_extra={"example": {
        "user_id": "l1", "name": "Dr Nkosi", "email": "nkosi@uni.ac.za",
        "password": "securepass", "department": "Computer Science", "employee_number": "EMP001",
    }})


class LoginRequest(BaseModel):
    email: str = Field(..., description="Registered email address")
    password: str = Field(..., description="Account password")
    role: str = Field(..., description="STUDENT or LECTURER")
    model_config = ConfigDict(json_schema_extra={"example": {
        "email": "alice@uni.ac.za", "password": "securepass", "role": "STUDENT"
    }})


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(None, description="New display name")
    email: Optional[str] = Field(None, description="New email address")
    model_config = ConfigDict(json_schema_extra={"example": {"name": "Alice Updated"}})


class StudentResponse(BaseModel):
    user_id: str
    name: str
    email: str
    student_number: str
    year_of_study: int
    role: str
    is_active: bool

    @classmethod
    def from_domain(cls, student) -> "StudentResponse":
        return cls(user_id=student.user_id, name=student.name, email=student.email,
                   student_number=student.student_number, year_of_study=student.year_of_study,
                   role=student.role, is_active=student.is_active)


class LecturerResponse(BaseModel):
    user_id: str
    name: str
    email: str
    department: str
    employee_number: str
    role: str
    is_active: bool

    @classmethod
    def from_domain(cls, lecturer) -> "LecturerResponse":
        return cls(user_id=lecturer.user_id, name=lecturer.name, email=lecturer.email,
                   department=lecturer.department, employee_number=lecturer.employee_number,
                   role=lecturer.role, is_active=lecturer.is_active)


class LoginResponse(BaseModel):
    message: str
    user_id: str
    role: str
    name: str


class CreateAssignmentRequest(BaseModel):
    lecturer_id: str = Field(..., description="ID of the creating lecturer")
    course_id: str = Field(..., description="ID of the target course")
    title: str = Field(..., description="Assignment title")
    description: str = Field(..., description="Full task description")
    due_date: date = Field(..., description="Submission deadline")
    total_marks: int = Field(..., gt=0, description="Maximum achievable score")
    model_config = ConfigDict(json_schema_extra={"example": {
        "lecturer_id": "l1", "course_id": "c1", "title": "Domain Model Assignment",
        "description": "Build a domain model for the system.",
        "due_date": "2026-06-01", "total_marks": 100,
    }})


class UpdateAssignmentRequest(BaseModel):
    lecturer_id: str = Field(..., description="ID of the owning lecturer")
    title: Optional[str] = Field(None, description="New title")
    due_date: Optional[date] = Field(None, description="New due date")
    model_config = ConfigDict(json_schema_extra={"example": {
        "lecturer_id": "l1", "title": "Updated Title", "due_date": "2026-06-15"
    }})


class AssignmentActionRequest(BaseModel):
    lecturer_id: str = Field(..., description="ID of the acting lecturer")
    model_config = ConfigDict(json_schema_extra={"example": {"lecturer_id": "l1"}})


class AssignmentResponse(BaseModel):
    assignment_id: str
    title: str
    description: str
    due_date: date
    total_marks: int
    status: str
    course_id: str
    lecturer_id: str

    @classmethod
    def from_domain(cls, assignment) -> "AssignmentResponse":
        return cls(assignment_id=assignment.assignment_id, title=assignment.title,
                   description=assignment.description, due_date=assignment.due_date,
                   total_marks=assignment.total_marks, status=assignment.status,
                   course_id=assignment.course.course_id,
                   lecturer_id=assignment._lecturer.user_id)


class SubmitAssignmentRequest(BaseModel):
    student_id: str = Field(..., description="ID of the submitting student")
    file_url: str = Field(..., description="URL of the submitted file")
    model_config = ConfigDict(json_schema_extra={"example": {
        "student_id": "s1", "file_url": "https://github.com/student/repo"
    }})


class GradeSubmissionRequest(BaseModel):
    lecturer_id: str = Field(..., description="ID of the grading lecturer")
    score: float = Field(..., ge=0, description="Numeric mark awarded")
    feedback: str = Field(..., description="Qualitative feedback comments")
    model_config = ConfigDict(json_schema_extra={"example": {
        "lecturer_id": "l1", "score": 85.0, "feedback": "Well structured."
    }})


class SubmissionResponse(BaseModel):
    submission_id: str
    student_id: str
    assignment_id: str
    submission_date: str
    file_url: str
    status: str

    @classmethod
    def from_domain(cls, submission) -> "SubmissionResponse":
        return cls(submission_id=submission.submission_id,
                   student_id=submission.student.user_id,
                   assignment_id=submission.assignment.assignment_id,
                   submission_date=str(submission.submission_date),
                   file_url=submission.file_url, status=submission.status)


class GradeResponse(BaseModel):
    grade_id: str
    submission_id: str
    score: float
    feedback: str
    graded_date: str
    percentage: Optional[float] = None

    @classmethod
    def from_domain(cls, grade, total_marks: int = None) -> "GradeResponse":
        return cls(grade_id=grade.grade_id,
                   submission_id=grade._submission.submission_id,
                   score=grade.score, feedback=grade.feedback,
                   graded_date=str(grade.graded_date),
                   percentage=grade.get_percentage(total_marks) if total_marks else None)


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: str