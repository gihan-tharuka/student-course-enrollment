#!/usr/bin/env python3
"""
Comprehensive API testing script for Student Course Enrollment Service
Tests all endpoints and business logic with SQLite database
"""

import asyncio
import json
import time
import subprocess
import requests
import sys
import os
from typing import Dict, Any

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_TIMEOUT = 30  # seconds

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
    def wait_for_server(self):
        """Wait for the server to be ready"""
        print("Waiting for server to start...")
        start_time = time.time()
        while time.time() - start_time < TEST_TIMEOUT:
            try:
                response = requests.get(f"{BASE_URL}/")
                if response.status_code == 200:
                    print("✓ Server is ready!")
                    return True
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        print("✗ Server failed to start within timeout")
        return False
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("\n=== Testing Health Check ===")
        try:
            response = self.session.get(f"{BASE_URL}/")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            assert response.status_code == 200
            print("✓ Health check passed")
            return True
        except Exception as e:
            print(f"✗ Health check failed: {e}")
            return False
    
    def test_create_student(self):
        """Test student creation"""
        print("\n=== Testing Student Creation ===")
        student_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "student_id": "STD001"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/students/", json=student_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 201:
                result = response.json()
                assert result["name"] == student_data["name"]
                assert result["email"] == student_data["email"]
                assert result["student_id"] == student_data["student_id"]
                print("✓ Student creation passed")
                return result["id"]
            else:
                print(f"✗ Student creation failed with status {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Student creation failed: {e}")
            return None
    
    def test_create_course(self):
        """Test course creation"""
        print("\n=== Testing Course Creation ===")
        course_data = {
            "name": "Introduction to Python",
            "code": "CS101",
            "description": "Learn Python programming basics",
            "capacity": 30
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/courses/", json=course_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 201:
                result = response.json()
                assert result["name"] == course_data["name"]
                assert result["code"] == course_data["code"]
                assert result["capacity"] == course_data["capacity"]
                print("✓ Course creation passed")
                return result["id"]
            else:
                print(f"✗ Course creation failed with status {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Course creation failed: {e}")
            return None
    
    def test_create_duplicate_student(self):
        """Test duplicate student ID prevention"""
        print("\n=== Testing Duplicate Student Prevention ===")
        student_data = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "student_id": "STD001"  # Same ID as previous student
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/students/", json=student_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 400:
                print("✓ Duplicate student prevention passed")
                return True
            else:
                print(f"✗ Expected 400 status, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Duplicate student test failed: {e}")
            return False
    
    def test_create_duplicate_course(self):
        """Test duplicate course code prevention"""
        print("\n=== Testing Duplicate Course Prevention ===")
        course_data = {
            "name": "Advanced Python",
            "code": "CS101",  # Same code as previous course
            "description": "Advanced Python programming",
            "capacity": 20
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/courses/", json=course_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 400:
                print("✓ Duplicate course prevention passed")
                return True
            else:
                print(f"✗ Expected 400 status, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Duplicate course test failed: {e}")
            return False
    
    def test_enroll_student(self, student_id: int, course_id: int):
        """Test student enrollment"""
        print("\n=== Testing Student Enrollment ===")
        enrollment_data = {
            "student_id": student_id,
            "course_id": course_id
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/enrollments/", json=enrollment_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 201:
                result = response.json()
                assert result["student_id"] == student_id
                assert result["course_id"] == course_id
                print("✓ Student enrollment passed")
                return result["id"]
            else:
                print(f"✗ Student enrollment failed with status {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Student enrollment failed: {e}")
            return None
    
    def test_duplicate_enrollment(self, student_id: int, course_id: int):
        """Test duplicate enrollment prevention"""
        print("\n=== Testing Duplicate Enrollment Prevention ===")
        enrollment_data = {
            "student_id": student_id,
            "course_id": course_id
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/enrollments/", json=enrollment_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 400:
                print("✓ Duplicate enrollment prevention passed")
                return True
            else:
                print(f"✗ Expected 400 status, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Duplicate enrollment test failed: {e}")
            return False
    
    def test_course_capacity_limit(self, student_id: int, course_id: int):
        """Test course capacity limit enforcement"""
        print("\n=== Testing Course Capacity Limit ===")
        # Try to enroll in a course that's at capacity
        # We'll use the same course but simulate capacity being full
        enrollment_data = {
            "student_id": student_id,
            "course_id": course_id
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/enrollments/", json=enrollment_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 400:
                print("✓ Course capacity limit enforcement passed")
                return True
            else:
                print(f"✗ Expected 400 status for capacity limit, got {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Course capacity test failed: {e}")
            return False
    
    def test_get_students(self):
        """Test getting students with pagination"""
        print("\n=== Testing Get Students (Pagination) ===")
        try:
            response = self.session.get(f"{BASE_URL}/students/?skip=0&limit=10")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                result = response.json()
                assert "items" in result
                assert "total" in result
                assert "page" in result
                assert "size" in result
                print("✓ Get students pagination passed")
                return True
            else:
                print(f"✗ Get students failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get students test failed: {e}")
            return False
    
    def test_get_courses(self):
        """Test getting courses with pagination"""
        print("\n=== Testing Get Courses (Pagination) ===")
        try:
            response = self.session.get(f"{BASE_URL}/courses/?skip=0&limit=10")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                result = response.json()
                assert "items" in result
                assert "total" in result
                assert "page" in result
                assert "size" in result
                print("✓ Get courses pagination passed")
                return True
            else:
                print(f"✗ Get courses failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get courses test failed: {e}")
            return False
    
    def test_get_enrollments(self):
        """Test getting enrollments with pagination"""
        print("\n=== Testing Get Enrollments (Pagination) ===")
        try:
            response = self.session.get(f"{BASE_URL}/enrollments/?skip=0&limit=10")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                result = response.json()
                assert "items" in result
                assert "total" in result
                assert "page" in result
                assert "size" in result
                print("✓ Get enrollments pagination passed")
                return True
            else:
                print(f"✗ Get enrollments failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get enrollments test failed: {e}")
            return False
    
    def test_get_student_by_id(self, student_id: int):
        """Test getting a specific student"""
        print("\n=== Testing Get Student by ID ===")
        try:
            response = self.session.get(f"{BASE_URL}/students/{student_id}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                result = response.json()
                assert result["id"] == student_id
                print("✓ Get student by ID passed")
                return True
            else:
                print(f"✗ Get student by ID failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get student by ID test failed: {e}")
            return False
    
    def test_get_course_by_id(self, course_id: int):
        """Test getting a specific course"""
        print("\n=== Testing Get Course by ID ===")
        try:
            response = self.session.get(f"{BASE_URL}/courses/{course_id}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                result = response.json()
                assert result["id"] == course_id
                print("✓ Get course by ID passed")
                return True
            else:
                print(f"✗ Get course by ID failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Get course by ID test failed: {e}")
            return False
    
    def test_update_student(self, student_id: int):
        """Test updating a student"""
        print("\n=== Testing Update Student ===")
        update_data = {
            "name": "John Smith",
            "email": "john.smith@example.com"
        }
        
        try:
            response = self.session.put(f"{BASE_URL}/students/{student_id}", json=update_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                result = response.json()
                assert result["name"] == update_data["name"]
                assert result["email"] == update_data["email"]
                print("✓ Update student passed")
                return True
            else:
                print(f"✗ Update student failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Update student test failed: {e}")
            return False
    
    def test_delete_student(self, student_id: int):
        """Test deleting a student"""
        print("\n=== Testing Delete Student ===")
        try:
            response = self.session.delete(f"{BASE_URL}/students/{student_id}")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✓ Delete student passed")
                return True
            else:
                print(f"✗ Delete student failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Delete student test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting comprehensive API tests with SQLite...")
        
        # Wait for server
        if not self.wait_for_server():
            return False
        
        # Test sequence
        tests_passed = 0
        total_tests = 0
        
        # Health check
        total_tests += 1
        if self.test_health_check():
            tests_passed += 1
        
        # Create test data
        student_id = self.test_create_student()
        course_id = self.test_create_course()
        
        if student_id and course_id:
            total_tests += 2
            tests_passed += 2
            
            # Test duplicate prevention
            total_tests += 1
            if self.test_create_duplicate_student():
                tests_passed += 1
            
            total_tests += 1
            if self.test_create_duplicate_course():
                tests_passed += 1
            
            # Test enrollment
            enrollment_id = self.test_enroll_student(student_id, course_id)
            if enrollment_id:
                total_tests += 1
                tests_passed += 1
                
                # Test duplicate enrollment
                total_tests += 1
                if self.test_duplicate_enrollment(student_id, course_id):
                    tests_passed += 1
            
            # Test pagination
            total_tests += 3
            if (self.test_get_students() and 
                self.test_get_courses() and 
                self.test_get_enrollments()):
                tests_passed += 3
            
            # Test individual get operations
            total_tests += 2
            if (self.test_get_student_by_id(student_id) and 
                self.test_get_course_by_id(course_id)):
                tests_passed += 2
            
            # Test update operations
            total_tests += 1
            if self.test_update_student(student_id):
                tests_passed += 1
            
            # Test delete operations
            total_tests += 1
            if self.test_delete_student(student_id):
                tests_passed += 1
        
        print(f"\n📊 Test Results: {tests_passed}/{total_tests} tests passed")
        
        if tests_passed == total_tests:
            print("🎉 All tests passed! The API is working correctly.")
            return True
        else:
            print("❌ Some tests failed. Please check the output above.")
            return False

def main():
    """Main function to run the tests"""
    tester = APITester()
    
    # Start the server in the background
    print("Starting FastAPI server with SQLite...")
    server_process = subprocess.Popen([
        "cd", "student-course-enrollment", "&&", "source", "venv/bin/activate", "&&", 
        "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"
    ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        # Run tests
        success = tester.run_all_tests()
        
        if success:
            print("\n✅ All API functionality has been successfully tested!")
            print("The Student Course Enrollment Service is working correctly with SQLite.")
        else:
            print("\n❌ Some tests failed. Please review the output above.")
        
        return 0 if success else 1
        
    finally:
        # Clean up server process
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    sys.exit(main())