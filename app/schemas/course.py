from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseBase(BaseModel):
    title: str
    code: str
    capacity: int = 30


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    capacity: Optional[int] = None


class CourseResponse(CourseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True