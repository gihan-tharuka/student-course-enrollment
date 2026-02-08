from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database.session import get_db
from ..services.course_service import CourseService
from ..schemas.course import CourseCreate, CourseResponse, CourseUpdate
from ..models import Course

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new course"""
    course_service = CourseService(db)
    
    # Check if course code already exists
    existing_course = await db.execute(
        Course.__table__.select().where(Course.code == course_data.code)
    )
    if existing_course.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )
    
    return await course_service.create_course(course_data)


@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all courses with pagination"""
    course_service = CourseService(db)
    courses = await course_service.get_courses(skip=skip, limit=limit)
    return courses


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course_by_id(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get course by ID"""
    course_service = CourseService(db)
    course = await course_service.get_course_by_id(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return course


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update course information"""
    course_service = CourseService(db)
    course = await course_service.update_course(course_id, course_data)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete course by ID"""
    course_service = CourseService(db)
    deleted = await course_service.delete_course(course_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return None