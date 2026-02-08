from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database.session import get_db
from ..services.student_service import StudentService
from ..schemas.student import StudentCreate, StudentResponse, StudentUpdate
from ..models import Student

router = APIRouter(
    prefix="/students",
    tags=["students"]
)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new student"""
    student_service = StudentService(db)
    
    # Check if email already exists
    existing_student = await db.execute(
        Student.__table__.select().where(Student.email == student_data.email)
    )
    if existing_student.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return await student_service.create_student(student_data)


@router.get("/", response_model=List[StudentResponse])
async def get_students(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all students with pagination"""
    student_service = StudentService(db)
    students = await student_service.get_students(skip=skip, limit=limit)
    return students


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_by_id(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get student by ID"""
    student_service = StudentService(db)
    student = await student_service.get_student_by_id(student_id)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return student


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update student information"""
    student_service = StudentService(db)
    student = await student_service.update_student(student_id, student_data)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete student by ID"""
    student_service = StudentService(db)
    deleted = await student_service.delete_student(student_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return None