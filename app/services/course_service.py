from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from ..models import Course
from ..schemas.course import CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_course(self, course_data: CourseCreate) -> Course:
        """Create a new course"""
        course = Course(**course_data.dict())
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def get_course_by_id(self, course_id: int) -> Optional[Course]:
        """Get course by ID"""
        result = await self.db.execute(
            select(Course).where(Course.id == course_id)
        )
        return result.scalar_one_or_none()

    async def get_course_by_code(self, course_code: str) -> Optional[Course]:
        """Get course by code"""
        result = await self.db.execute(
            select(Course).where(Course.code == course_code)
        )
        return result.scalar_one_or_none()

    async def get_courses(self, skip: int = 0, limit: int = 100) -> List[Course]:
        """Get all courses with pagination"""
        result = await self.db.execute(
            select(Course)
            .offset(skip)
            .limit(limit)
            .order_by(Course.id)
        )
        return result.scalars().all()

    async def update_course(self, course_id: int, course_data: CourseUpdate) -> Optional[Course]:
        """Update course information"""
        course = await self.get_course_by_id(course_id)
        if not course:
            return None

        update_data = course_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)

        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def delete_course(self, course_id: int) -> bool:
        """Delete course by ID"""
        course = await self.get_course_by_id(course_id)
        if not course:
            return False

        await self.db.delete(course)
        await self.db.commit()
        return True

    async def get_course_count(self) -> int:
        """Get total count of courses"""
        result = await self.db.execute(select(func.count()).select_from(Course))
        return result.scalar_one()

    async def get_active_enrollment_count(self, course_id: int) -> int:
        """Get count of active enrollments for a course"""
        from ..models import Enrollment
        result = await self.db.execute(
            select(func.count())
            .select_from(Enrollment)
            .where(
                Enrollment.course_id == course_id,
                Enrollment.status == "active"
            )
        )
        return result.scalar_one()