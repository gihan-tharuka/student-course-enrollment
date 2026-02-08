from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..database.session import get_db
from ..services.enrollment_service import EnrollmentService
from ..schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentUpdate
from ..models import Enrollment

router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"]
)


@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_student(
    enrollment_data: EnrollmentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Enroll a student in a course"""
    enrollment_service = EnrollmentService(db)
    return await enrollment_service.enroll_student(enrollment_data)


@router.get("/", response_model=List[EnrollmentResponse])
async def get_enrollments(
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get enrollments with optional filters and pagination"""
    enrollment_service = EnrollmentService(db)
    enrollments = await enrollment_service.get_enrollments(
        student_id=student_id,
        course_id=course_id,
        status_filter=status_filter,
        skip=skip,
        limit=limit
    )
    return enrollments


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
async def get_enrollment_by_id(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get enrollment by ID"""
    enrollment_service = EnrollmentService(db)
    enrollment = await enrollment_service.get_enrollment_by_id(enrollment_id)
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    return enrollment


@router.patch("/{enrollment_id}/cancel", response_model=EnrollmentResponse)
async def cancel_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Cancel an enrollment"""
    enrollment_service = EnrollmentService(db)
    enrollment = await enrollment_service.cancel_enrollment(enrollment_id)
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    return enrollment