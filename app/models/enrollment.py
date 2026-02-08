from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.session import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False, default="active")  # active or cancelled
    enrolled_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship with student and course
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    # Unique constraint to prevent duplicate enrollments
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='unique_student_course'),
    )

    def __repr__(self):
        return f"<Enrollment(id={self.id}, student_id={self.student_id}, course_id={self.course_id}, status='{self.status}')>"