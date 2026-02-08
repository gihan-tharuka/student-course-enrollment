from .students import router as students_router
from .courses import router as courses_router
from .enrollments import router as enrollments_router

__all__ = ["students_router", "courses_router", "enrollments_router"]