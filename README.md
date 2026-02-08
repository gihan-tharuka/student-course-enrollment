# Student Course Enrollment Service

A REST API for managing student course enrollments built with Python + FastAPI, PostgreSQL, and SQLAlchemy ORM.

## Features

- **Students Management**: Create, read, update, and delete students
- **Courses Management**: Create, read, update, and delete courses with capacity limits
- **Enrollment Management**: Enroll students in courses with business rule validation
- **Business Rules**:
  - Prevent duplicate enrollments (same student + same course)
  - Enforce course capacity limits for active enrollments
  - Cancelled enrollments don't count toward capacity
- **Pagination**: All list endpoints support pagination
- **Validation**: Comprehensive request validation with Pydantic
- **Error Handling**: Proper HTTP status codes and meaningful error messages

## Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern web framework
- **PostgreSQL** - Database
- **SQLAlchemy ORM** - Database ORM (async)
- **Pydantic** - Data validation
- **Docker Compose** - Database setup

## Project Structure

```
student-course-enrollment/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── models/                    # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── course.py
│   │   └── enrollment.py
│   ├── schemas/                   # Pydantic models
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── course.py
│   │   └── enrollment.py
│   ├── database/                  # Database configuration
│   │   ├── __init__.py
│   │   └── session.py
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── student_service.py
│   │   ├── course_service.py
│   │   └── enrollment_service.py
│   ├── routers/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── students.py
│   │   ├── courses.py
│   │   └── enrollments.py
│   └── dependencies.py            # Dependency injection
├── tests/                         # Unit tests
│   ├── __init__.py
│   ├── test_students.py
│   ├── test_courses.py
│   └── test_enrollments.py
├── .env.example                   # Environment variables template
├── .gitignore
├── README.md                      # This file
├── requirements.txt               # Python dependencies
└── docker-compose.yml            # PostgreSQL setup
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd student-course-enrollment
```

### 2. Set up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Option A: Using Docker Compose (Recommended)

```bash
# Start PostgreSQL database
docker-compose up -d

# Verify database is running
docker-compose ps
```

#### Option B: Manual PostgreSQL Installation

1. Install PostgreSQL on your system
2. Create a database: `student_enrollment_db`
3. Create a user with appropriate permissions

### 5. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your database configuration
# Default for Docker Compose:
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/student_enrollment_db
```

### 6. Run the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Students

- `POST /students/` - Create a new student
- `GET /students/` - Get all students (with pagination)
- `GET /students/{id}` - Get student by ID
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

### Courses

- `POST /courses/` - Create a new course
- `GET /courses/` - Get all courses (with pagination)
- `GET /courses/{id}` - Get course by ID
- `PUT /courses/{id}` - Update course
- `DELETE /courses/{id}` - Delete course

### Enrollments

- `POST /enrollments/` - Enroll a student in a course
- `GET /enrollments/` - Get enrollments (with filters and pagination)
- `GET /enrollments/{id}` - Get enrollment by ID
- `PATCH /enrollments/{id}/cancel` - Cancel enrollment

## Example Usage

### Create a Student

```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john.doe@example.com"
  }'
```

### Create a Course

```bash
curl -X POST "http://localhost:8000/courses/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Python",
    "code": "CS101",
    "capacity": 30
  }'
```

### Enroll a Student in a Course

```bash
curl -X POST "http://localhost:8000/enrollments/" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "course_id": 1
  }'
```

### Get All Students with Pagination

```bash
curl "http://localhost:8000/students/?skip=0&limit=10"
```

### Get Enrollments with Filters

```bash
curl "http://localhost:8000/enrollments/?student_id=1&status=active"
```

### Cancel an Enrollment

```bash
curl -X PATCH "http://localhost:8000/enrollments/1/cancel"
```

## Business Rules Validation

The API enforces the following business rules:

1. **Duplicate Enrollment Prevention**: 
   - Error: "Student already enrolled in this course"
   - Status Code: 400

2. **Course Capacity Enforcement**:
   - Error: "Course capacity reached"
   - Status Code: 400

3. **Email Uniqueness**:
   - Error: "Email already registered"
   - Status Code: 400

4. **Course Code Uniqueness**:
   - Error: "Course code already exists"
   - Status Code: 400

5. **Resource Not Found**:
   - Error: "Student not found", "Course not found", "Enrollment not found"
   - Status Code: 404

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_students.py
```

## Database Schema

### Students Table
- `id` (Primary Key, Integer)
- `full_name` (String, Required)
- `email` (String, Unique, Required)
- `created_at` (DateTime)

### Courses Table
- `id` (Primary Key, Integer)
- `title` (String, Required)
- `code` (String, Unique, Required)
- `capacity` (Integer, Required, Default: 30)
- `created_at` (DateTime)

### Enrollments Table
- `id` (Primary Key, Integer)
- `student_id` (Foreign Key → Students.id)
- `course_id` (Foreign Key → Courses.id)
- `status` (String: "active" or "cancelled", Default: "active")
- `enrolled_at` (DateTime)
- `created_at` (DateTime)

**Constraints:**
- Unique constraint on (student_id, course_id)
- Foreign key constraints with CASCADE DELETE
- Check constraint for positive capacity

## Development

### Code Style
- Use Black for code formatting
- Use isort for import sorting
- Follow PEP 8 guidelines

### Adding New Features
1. Create database models in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/routers/`
5. Add tests in `tests/`

## Deployment

### Production Environment
1. Set `DEBUG=False` in environment variables
2. Use a production PostgreSQL instance
3. Configure proper CORS origins
4. Use a production ASGI server (e.g., Gunicorn)
5. Set up reverse proxy (e.g., Nginx)

### Docker Deployment
```bash
# Build Docker image
docker build -t student-enrollment-api .

# Run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`