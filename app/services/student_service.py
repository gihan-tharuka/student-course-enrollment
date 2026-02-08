from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..models import Student
from ..schemas.student import StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_student(self, student_data: StudentCreate) -> Student:
        """Create a new student"""
        student = Student(**student_data.dict())
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        result = await self.db.execute(
            select(Student).where(Student.id == student_id)
        )
        return result.scalar_one_or_none()

    async def get_students(self, skip: int = 0, limit: int = 100) -> List[Student]:
        """Get all students with pagination"""
        result = await self.db.execute(
            select(Student)
            .offset(skip)
            .limit(limit)
            .order_by(Student.id)
        )
        return result.scalars().all()

    async def update_student(self, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
        """Update student information"""
        student = await self.get_student_by_id(student_id)
        if not student:
            return None

        update_data = student_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)

        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def delete_student(self, student_id: int) -> bool:
        """Delete student by ID"""
        student = await self.get_student_by_id(student_id)
        if not student:
            return False

        await self.db.delete(student)
        await self.db.commit()
        return True

    async def get_student_count(self) -> int:
        """Get total count of students"""
        result = await self.db.execute(select(func.count()).select_from(Student))
        return result.scalar_one()