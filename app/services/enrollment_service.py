from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from ..models import Enrollment, Student, Course
from ..schemas.enrollment import EnrollmentCreate
from fastapi import HTTPException, status


class EnrollmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def enroll_student(self, enrollment_data: EnrollmentCreate) -> Enrollment:
        """Enroll a student in a course with business rule validation"""
        # Check if student exists
        student_result = await self.db.execute(
            select(Student).where(Student.id == enrollment_data.student_id)
        )
        student = student_result.scalar_one_or_none()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        # Check if course exists
        course_result = await self.db.execute(
            select(Course).where(Course.id == enrollment_data.course_id)
        )
        course = course_result.scalar_one_or_none()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )

        # Check if student is already enrolled in this course
        existing_enrollment_result = await self.db.execute(
            select(Enrollment).where(
                Enrollment.student_id == enrollment_data.student_id,
                Enrollment.course_id == enrollment_data.course_id
            )
        )
        existing_enrollment = existing_enrollment_result.scalar_one_or_none()
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already enrolled in this course"
            )

        # Check course capacity
        active_enrollment_count = await self.get_active_enrollment_count(enrollment_data.course_id)
        if active_enrollment_count >= course.capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course capacity reached"
            )

        # Create enrollment
        enrollment = Enrollment(**enrollment_data.dict())
        self.db.add(enrollment)
        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment

    async def get_enrollment_by_id(self, enrollment_id: int) -> Optional[Enrollment]:
        """Get enrollment by ID"""
        result = await self.db.execute(
            select(Enrollment).where(Enrollment.id == enrollment_id)
        )
        return result.scalar_one_or_none()

    async def get_enrollments(self, 
                            student_id: Optional[int] = None,
                            course_id: Optional[int] = None,
                            status_filter: Optional[str] = None,
                            skip: int = 0, 
                            limit: int = 100) -> List[Enrollment]:
        """Get enrollments with optional filters and pagination"""
        query = select(Enrollment)
        
        if student_id:
            query = query.where(Enrollment.student_id == student_id)
        if course_id:
            query = query.where(Enrollment.course_id == course_id)
        if status_filter:
            query = query.where(Enrollment.status == status_filter)

        query = query.offset(skip).limit(limit).order_by(Enrollment.id)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def cancel_enrollment(self, enrollment_id: int) -> Optional[Enrollment]:
        """Cancel an enrollment by setting status to 'cancelled'"""
        enrollment = await self.get_enrollment_by_id(enrollment_id)
        if not enrollment:
            return None

        enrollment.status = "cancelled"
        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment

    async def get_enrollment_count(self, 
                                  student_id: Optional[int] = None,
                                  course_id: Optional[int] = None,
                                  status_filter: Optional[str] = None) -> int:
        """Get total count of enrollments with optional filters"""
        query = select(func.count()).select_from(Enrollment)
        
        if student_id:
            query = query.where(Enrollment.student_id == student_id)
        if course_id:
            query = query.where(Enrollment.course_id == course_id)
        if status_filter:
            query = query.where(Enrollment.status == status_filter)

        result = await self.db.execute(query)
        return result.scalar_one()

    async def get_active_enrollment_count(self, course_id: int) -> int:
        """Get count of active enrollments for a course"""
        result = await self.db.execute(
            select(func.count())
            .select_from(Enrollment)
            .where(
                Enrollment.course_id == course_id,
                Enrollment.status == "active"
            )
        )
        return result.scalar_one()