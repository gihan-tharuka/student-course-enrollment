#!/usr/bin/env python3
"""
Simple structure validation script to verify the project structure
without requiring external dependencies.
"""

import os
import sys
from pathlib import Path

def check_file_exists(path, description):
    """Check if a file exists and print result"""
    if os.path.exists(path):
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (NOT FOUND)")
        return False

def main():
    """Validate project structure"""
    base_path = Path(__file__).parent
    print("Validating Student Course Enrollment Service Structure...\n")
    
    # Check main files
    files_to_check = [
        (base_path / "requirements.txt", "Requirements file"),
        (base_path / ".env.example", "Environment template"),
        (base_path / ".gitignore", "Git ignore file"),
        (base_path / "docker-compose.yml", "Docker Compose setup"),
        (base_path / "README.md", "Documentation"),
        (base_path / "app" / "__init__.py", "App package"),
        (base_path / "app" / "main.py", "Main application"),
        (base_path / "app" / "database" / "__init__.py", "Database package"),
        (base_path / "app" / "database" / "session.py", "Database session"),
        (base_path / "app" / "models" / "__init__.py", "Models package"),
        (base_path / "app" / "models" / "student.py", "Student model"),
        (base_path / "app" / "models" / "course.py", "Course model"),
        (base_path / "app" / "models" / "enrollment.py", "Enrollment model"),
        (base_path / "app" / "schemas" / "__init__.py", "Schemas package"),
        (base_path / "app" / "schemas" / "student.py", "Student schema"),
        (base_path / "app" / "schemas" / "course.py", "Course schema"),
        (base_path / "app" / "schemas" / "enrollment.py", "Enrollment schema"),
        (base_path / "app" / "services" / "__init__.py", "Services package"),
        (base_path / "app" / "services" / "student_service.py", "Student service"),
        (base_path / "app" / "services" / "course_service.py", "Course service"),
        (base_path / "app" / "services" / "enrollment_service.py", "Enrollment service"),
        (base_path / "app" / "routers" / "__init__.py", "Routers package"),
        (base_path / "app" / "routers" / "students.py", "Students router"),
        (base_path / "app" / "routers" / "courses.py", "Courses router"),
        (base_path / "app" / "routers" / "enrollments.py", "Enrollments router"),
        (base_path / "tests" / "__init__.py", "Tests package"),
        (base_path / "tests" / "test_students.py", "Student tests"),
    ]
    
    all_found = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_found = False
    
    print(f"\n{'='*50}")
    if all_found:
        print("✓ All required files found! Project structure is complete.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up database: docker-compose up -d")
        print("3. Configure environment: cp .env.example .env")
        print("4. Run the application: uvicorn app.main:app --reload")
        print("5. View API docs: http://localhost:8000/docs")
    else:
        print("✗ Some files are missing. Please check the structure above.")
        sys.exit(1)

if __name__ == "__main__":
    main()