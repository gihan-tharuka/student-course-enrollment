import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from app.main import app
from app.database.session import get_db, Base
from app.models import Student

# Test database URL for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine and session
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestAsyncSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    async with TestAsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
async def setup_database():
    """Setup test database"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_student(setup_database):
    """Test creating a new student"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/students/", json={
            "full_name": "John Doe",
            "email": "john@example.com"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["full_name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data


@pytest.mark.asyncio
async def test_get_students(setup_database):
    """Test getting all students"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/students/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_student_by_id(setup_database):
    """Test getting student by ID"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create a student
        create_response = await client.post("/students/", json={
            "full_name": "Jane Doe",
            "email": "jane@example.com"
        })
        
        student_id = create_response.json()["id"]
        
        # Get the student
        response = await client.get(f"/students/{student_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == student_id
        assert data["full_name"] == "Jane Doe"


@pytest.mark.asyncio
async def test_update_student(setup_database):
    """Test updating a student"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create a student
        create_response = await client.post("/students/", json={
            "full_name": "Bob Smith",
            "email": "bob@example.com"
        })
        
        student_id = create_response.json()["id"]
        
        # Update the student
        response = await client.put(f"/students/{student_id}", json={
            "full_name": "Robert Smith"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Robert Smith"


@pytest.mark.asyncio
async def test_delete_student(setup_database):
    """Test deleting a student"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create a student
        create_response = await client.post("/students/", json={
            "full_name": "Alice Johnson",
            "email": "alice@example.com"
        })
        
        student_id = create_response.json()["id"]
        
        # Delete the student
        response = await client.delete(f"/students/{student_id}")
        
        assert response.status_code == 204