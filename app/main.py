from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine
from .database.session import Base, engine
from .routers import students_router, courses_router, enrollments_router
import os
from dotenv import load_dotenv

load_dotenv()

# Create database tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await create_tables()
    yield
    # Shutdown: Cleanup if needed


app = FastAPI(
    title="Student Course Enrollment Service",
    description="A REST API for managing student course enrollments",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(students_router)
app.include_router(courses_router)
app.include_router(enrollments_router)


@app.get("/")
async def root():
    return {
        "message": "Student Course Enrollment Service",
        "version": "1.0.0",
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}