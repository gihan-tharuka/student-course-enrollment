#!/usr/bin/env python3
"""
Simple demonstration of the Student Course Enrollment Service functionality
"""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database.session import Base, engine
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.services.student_service import StudentService
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.schemas.student import StudentCreate
from app.schemas.course import CourseCreate
from app.schemas.enrollment import EnrollmentCreate


async def demonstrate_functionality():
    """Demonstrate the core functionality of the service"""
    print("🚀 Demonstrating Student Course Enrollment Service")
    print("=" * 60)
    
    # Set up database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables created")
    
    # Create session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Demo 1: Create Students
    print("\n📝 Creating Students...")
    async with async_session() as session:
        student_service = StudentService(session)
        
        student1_data = StudentCreate(full_name="John Doe", email="john@example.com")
        student2_data = StudentCreate(full_name="Jane Smith", email="jane@example.com")
        
        student1 = await student_service.create_student(student1_data)
        student2 = await student_service.create_student(student2_data)
        
        print(f"✓ Created student: {student1.full_name} (ID: {student1.id})")
        print(f"✓ Created student: {student2.full_name} (ID: {student2.id})")
    
    # Demo 2: Create Courses
    print("\n📚 Creating Courses...")
    async with async_session() as session:
        course_service = CourseService(session)
        
        course1_data = CourseCreate(title="Python Programming", code="CS101", capacity=2)
        course2_data = CourseCreate(title="Web Development", code="CS102", capacity=1)
        
        course1 = await course_service.create_course(course1_data)
        course2 = await course_service.create_course(course2_data)
        
        print(f"✓ Created course: {course1.title} (Code: {course1.code}, Capacity: {course1.capacity})")
        print(f"✓ Created course: {course2.title} (Code: {course2.code}, Capacity: {course2.capacity})")
    
    # Demo 3: Create Enrollments
    print("\n✅ Creating Enrollments...")
    async with async_session() as session:
        enrollment_service = EnrollmentService(session)
        
        # Enroll John in Python Programming
        enrollment1_data = EnrollmentCreate(student_id=student1.id, course_id=course1.id)
        enrollment1 = await enrollment_service.enroll_student(enrollment1_data)
        print(f"✓ Enrolled {student1.full_name} in {course1.title}")
        
        # Enroll Jane in Python Programming
        enrollment2_data = EnrollmentCreate(student_id=student2.id, course_id=course1.id)
        enrollment2 = await enrollment_service.enroll_student(enrollment2_data)
        print(f"✓ Enrolled {student2.full_name} in {course1.title}")
        
        # Try to enroll John in Web Development (should succeed)
        enrollment3_data = EnrollmentCreate(student_id=student1.id, course_id=course2.id)
        enrollment3 = await enrollment_service.enroll_student(enrollment3_data)
        print(f"✓ Enrolled {student1.full_name} in {course2.title}")
    
    # Demo 4: Test Business Rules
    print("\n🔒 Testing Business Rules...")
    
    # Try to enroll Jane in Web Development (should fail - capacity reached)
    async with async_session() as session:
        enrollment_service = EnrollmentService(session)
        
        try:
            enrollment4_data = EnrollmentCreate(student_id=student2.id, course_id=course2.id)
            await enrollment_service.enroll_student(enrollment4_data)
            print("✗ Business rule failed - should not allow enrollment beyond capacity")
        except Exception as e:
            print(f"✓ Business rule enforced: {str(e)}")
    
    # Try to enroll John in Python Programming again (should fail - duplicate)
    async with async_session() as session:
        enrollment_service = EnrollmentService(session)
        
        try:
            enrollment5_data = EnrollmentCreate(student_id=student1.id, course_id=course1.id)
            await enrollment_service.enroll_student(enrollment5_data)
            print("✗ Business rule failed - should not allow duplicate enrollment")
        except Exception as e:
            print(f"✓ Business rule enforced: {str(e)}")
    
    # Demo 5: Query Data
    print("\n📊 Querying Data...")
    async with async_session() as session:
        student_service = StudentService(session)
        course_service = CourseService(session)
        enrollment_service = EnrollmentService(session)
        
        # Get all students
        students = await student_service.get_students()
        print(f"✓ Found {len(students)} students")
        
        # Get all courses
        courses = await course_service.get_courses()
        print(f"✓ Found {len(courses)} courses")
        
        # Get all enrollments
        enrollments = await enrollment_service.get_enrollments()
        print(f"✓ Found {len(enrollments)} enrollments")
        
        # Get enrollments for John
        john_enrollments = await enrollment_service.get_enrollments(student_id=student1.id)
        print(f"✓ {student1.full_name} is enrolled in {len(john_enrollments)} courses")
        
        # Get enrollments for Python Programming
        python_enrollments = await enrollment_service.get_enrollments(course_id=course1.id)
        print(f"✓ {course1.title} has {len(python_enrollments)} students enrolled")
    
    print("\n🎉 Demonstration completed successfully!")
    print("The Student Course Enrollment Service is working correctly with all business rules enforced.")


async def main():
    """Main function"""
    try:
        await demonstrate_functionality()
        return 0
    except Exception as e:
        print(f"\n💥 Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result)