from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.session import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    capacity = Column(Integer, nullable=False, default=30)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship with enrollments
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    # Check constraint to ensure capacity is positive
    __table_args__ = (
        CheckConstraint('capacity > 0', name='check_capacity_positive'),
    )

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', code='{self.code}', capacity={self.capacity})>"