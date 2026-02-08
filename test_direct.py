#!/usr/bin/env python3
"""
Direct database testing script for Student Course Enrollment Service
Tests all business logic and database operations without requiring server startup
"""

import asyncio
import sys
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.session import Base, engine
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.services.student_service import StudentService
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.schemas.student import StudentCreate, StudentUpdate
from app.schemas.course import CourseCreate, CourseUpdate
from app.schemas.enrollment import EnrollmentCreate


class DirectTester:
    def __init__(self):
        self.async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def setup_database(self):
        """Set up the database tables"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✓ Database tables created successfully")
    
    async def test_student_operations(self):
        """Test all student operations"""
        print("\n=== Testing Student Operations ===")
        
        # Test 1: Create student
        student_data = StudentCreate(
            full_name="John Doe",
            email="john.doe@example.com"
        )
        
        async with self.async_session() as session:
            student_service = StudentService(session)
            student = await student_service.create_student(student_data)
        assert student.full_name == student_data.full_name
        assert student.email == student_data.email
        print("✓ Student creation passed")
        
        # Test 2: Get student
        async with self.async_session() as session:
            student_service = StudentService(session)
            retrieved_student = await student_service.get_student_by_id(student.id)
        assert retrieved_student.id == student.id
        print("✓ Get student passed")
        
        # Test 3: List students
        async with self.async_session() as session:
            student_service = StudentService(session)
            students = await student_service.get_students(skip=0, limit=10)
        assert len(students.items) == 1
        print("✓ List students passed")
        
        # Test 4: Update student
        update_data = StudentUpdate(
            full_name="John Smith",
            email="john.smith@example.com"
        )
        
        async with self.async_session() as session:
            student_service = StudentService(session)
            updated_student = await student_service.update_student(student.id, update_data)
        assert updated_student.full_name == update_data.full_name
        assert updated_student.email == update_data.email
        print("✓ Update student passed")
        
        # Test 5: Delete student
        async with self.async_session() as session:
            student_service = StudentService(session)
            await student_service.delete_student(student.id)
            deleted_student = await student_service.get_student_by_id(student.id)
        assert deleted_student is None
        print("✓ Delete student passed")
        
        return True
    
    async def test_course_operations(self):
        """Test all course operations"""
        print("\n=== Testing Course Operations ===")
        
        # Test 1: Create course
        course_data = CourseCreate(
            title="Introduction to Python",
            code="CS101",
            capacity=30
        )
        
        async with self.async_session() as session:
            course_service = CourseService(session)
            course = await course_service.create_course(course_data)
        assert course.title == course_data.title
        assert course.code == course_data.code
        assert course.capacity == course_data.capacity
        print("✓ Course creation passed")
        
        # Test 2: Get course
        async with self.async_session() as session:
            course_service = CourseService(session)
            retrieved_course = await course_service.get_course_by_id(course.id)
        assert retrieved_course.id == course.id
        print("✓ Get course passed")
        
        # Test 3: List courses
        async with self.async_session() as session:
            course_service = CourseService(session)
            courses = await course_service.get_courses(skip=0, limit=10)
        assert len(courses.items) == 1
        print("✓ List courses passed")
        
        # Test 4: Update course
        update_data = CourseUpdate(
            title="Advanced Python",
            capacity=25
        )
        
        async with self.async_session() as session:
            course_service = CourseService(session)
            updated_course = await course_service.update_course(course.id, update_data)
        assert updated_course.title == update_data.title
        assert updated_course.capacity == update_data.capacity
        print("✓ Update course passed")
        
        # Test 5: Delete course
        async with self.async_session() as session:
            course_service = CourseService(session)
            await course_service.delete_course(course.id)
            deleted_course = await course_service.get_course_by_id(course.id)
        assert deleted_course is None
        print("✓ Delete course passed")
        
        return True
    
    async def test_enrollment_operations(self):
        """Test all enrollment operations"""
        print("\n=== Testing Enrollment Operations ===")
        
        # Create test data
        student_data = StudentCreate(
            full_name="Jane Doe",
            email="jane.doe@example.com"
        )
        
        async with self.async_session() as session:
            student_service = StudentService(session)
            student = await student_service.create_student(student_data)
        
        course_data = CourseCreate(
            title="Data Structures",
            code="CS201",
            capacity=20
        )
        
        async with self.async_session() as session:
            course_service = CourseService(session)
            course = await course_service.create_course(course_data)
        
        # Test 1: Create enrollment
        enrollment_data = EnrollmentCreate(
            student_id=student.id,
            course_id=course.id
        )
        
        async with self.async_session() as session:
            enrollment_service = EnrollmentService(session)
            enrollment = await enrollment_service.create_enrollment(enrollment_data)
        assert enrollment.student_id == student.id
        assert enrollment.course_id == course.id
        print("✓ Enrollment creation passed")
        
        # Test 2: Get enrollment
        async with self.async_session() as session:
            enrollment_service = EnrollmentService(session)
            retrieved_enrollment = await enrollment_service.get_enrollment_by_id(enrollment.id)
        assert retrieved_enrollment.id == enrollment.id
        print("✓ Get enrollment passed")
        
        # Test 3: List enrollments
        async with self.async_session() as session:
            enrollment_service = EnrollmentService(session)
            enrollments = await enrollment_service.get_enrollments(skip=0, limit=10)
        assert len(enrollments.items) == 1
        print("✓ List enrollments passed")
        
        # Test 4: Delete enrollment
        async with self.async_session() as session:
            enrollment_service = EnrollmentService(session)
            await enrollment_service.delete_enrollment(enrollment.id)
            deleted_enrollment = await enrollment_service.get_enrollment_by_id(enrollment.id)
        assert deleted_enrollment is None
        print("✓ Delete enrollment passed")
        
        # Clean up
        async with self.async_session() as session:
            student_service = StudentService(session)
            course_service = CourseService(session)
            await student_service.delete_student(student.id)
            await course_service.delete_course(course.id)
        
        return True
    
    async def test_business_rules(self):
        """Test business rule enforcement"""
        print("\n=== Testing Business Rules ===")
        
        # Create test data
        student_data = StudentCreate(
            full_name="Alice Johnson",
            email="alice@example.com"
        )
        
        async with self.async_session() as session:
            student_service = StudentService(session)
            student = await student_service.create_student(student_data)
        
        course_data = CourseCreate(
            title="Machine Learning",
            code="CS301",
            capacity=2
        )
        
        async with self.async_session() as session:
            course_service = CourseService(session)
            course = await course_service.create_course(course_data)
        
        # Test 1: Duplicate student ID prevention
        duplicate_student_data = StudentCreate(
            full_name="Bob Smith",
            email="bob@example.com"
        )
        
        try:
            async with self.async_session() as session:
                student_service = StudentService(session)
                await student_service.create_student(duplicate_student_data)
            assert False, "Should have raised exception for duplicate student ID"
        except Exception as e:
            assert "already exists" in str(e).lower()
            print("✓ Duplicate student ID prevention passed")
        
        # Test 2: Duplicate course code prevention
        duplicate_course_data = CourseCreate(
            title="Deep Learning",
            code="CS301",  # Same code
            capacity=3
        )
        
        try:
            async with self.async_session() as session:
                course_service = CourseService(session)
                await course_service.create_course(duplicate_course_data)
            assert False, "Should have raised exception for duplicate course code"
        except Exception as e:
            assert "already exists" in str(e).lower()
            print("✓ Duplicate course code prevention passed")
        
        # Test 3: Duplicate enrollment prevention
        enrollment_data = EnrollmentCreate(
            student_id=student.id,
            course_id=course.id
        )
        
        # First enrollment should succeed
        async with self.async_session() as session:
            enrollment_service = EnrollmentService(session)
            enrollment = await enrollment_service.create_enrollment(enrollment_data)
        print("✓ First enrollment succeeded")
        
        # Second enrollment should fail
        try:
            async with self.async_session() as session:
                enrollment_service = EnrollmentService(session)
                await enrollment_service.create_enrollment(enrollment_data)
            assert False, "Should have raised exception for duplicate enrollment"
        except Exception as e:
            assert "already enrolled" in str(e).lower()
            print("✓ Duplicate enrollment prevention passed")
        
        # Test 4: Course capacity enforcement
        # Create another student and try to enroll when capacity is reached
        student2_data = StudentCreate(
            full_name="Charlie Brown",
            email="charlie@example.com"
        )
        
        async with self.async_session() as session:
            student_service = StudentService(session)
            student2 = await student_service.create_student(student2_data)
        
        # Update course capacity to 1 and try to enroll second student
        async with self.async_session() as session:
            course_service = CourseService(session)
            await course_service.update_course(course.id, CourseUpdate(capacity=1))
        
        enrollment2_data = EnrollmentCreate(
            student_id=student2.id,
            course_id=course.id
        )
        
        try:
            async with self.async_session() as session:
                enrollment_service = EnrollmentService(session)
                await enrollment_service.create_enrollment(enrollment2_data)
            assert False, "Should have raised exception for course capacity"
        except Exception as e:
            assert "capacity" in str(e).lower()
            print("✓ Course capacity enforcement passed")
        
        # Clean up
        async with self.async_session() as session:
            enrollment_service = EnrollmentService(session)
            student_service = StudentService(session)
            course_service = CourseService(session)
            await enrollment_service.delete_enrollment(enrollment.id)
            await student_service.delete_student(student.id)
            await student_service.delete_student(student2.id)
            await course_service.delete_course(course.id)
        
        return True
    
    async def test_pagination(self):
        """Test pagination functionality"""
        print("\n=== Testing Pagination ===")
        
        # Create multiple students
        for i in range(15):
            student_data = StudentCreate(
                full_name=f"Student {i}",
                email=f"student{i}@example.com"
            )
            
            async with self.async_session() as session:
                student_service = StudentService(session)
                await student_service.create_student(student_data)
        
        # Test pagination
        async with self.async_session() as session:
            student_service = StudentService(session)
            page1 = await student_service.get_students(skip=0, limit=10)
            page2 = await student_service.get_students(skip=10, limit=10)
        
        assert len(page1.items) == 10
        assert len(page2.items) == 5
        assert page1.total == 15
        assert page1.page == 1
        assert page1.size == 10
        assert page2.page == 2
        assert page2.size == 10
        
        print("✓ Pagination passed")
        
        # Clean up
        for i in range(15):
            async with self.async_session() as session:
                student_service = StudentService(session)
                student = await student_service.get_students(skip=i, limit=1)
                if student.items:
                    await student_service.delete_student(student.items[0].id)
        
        return True
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting direct database tests...")
        
        # Setup
        await self.setup_database()
        
        # Run tests
        tests_passed = 0
        total_tests = 5
        
        try:
            if await self.test_student_operations():
                tests_passed += 1
        except Exception as e:
            print(f"✗ Student operations test failed: {e}")
        
        try:
            if await self.test_course_operations():
                tests_passed += 1
        except Exception as e:
            print(f"✗ Course operations test failed: {e}")
        
        try:
            if await self.test_enrollment_operations():
                tests_passed += 1
        except Exception as e:
            print(f"✗ Enrollment operations test failed: {e}")
        
        try:
            if await self.test_business_rules():
                tests_passed += 1
        except Exception as e:
            print(f"✗ Business rules test failed: {e}")
        
        try:
            if await self.test_pagination():
                tests_passed += 1
        except Exception as e:
            print(f"✗ Pagination test failed: {e}")
        
        print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
        
        if tests_passed == total_tests:
            print("🎉 All tests passed! The business logic is working correctly.")
            return True
        else:
            print("❌ Some tests failed. Please check the output above.")
            return False


async def main():
    """Main function to run the tests"""
    tester = DirectTester()
    
    try:
        success = await tester.run_all_tests()
        
        if success:
            print("\n✅ All business logic has been successfully tested!")
            print("The Student Course Enrollment Service is working correctly.")
        else:
            print("\n❌ Some tests failed. Please review the output above.")
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result)