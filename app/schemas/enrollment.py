from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    status: str
    enrolled_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True