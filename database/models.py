from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_hard = Column(Boolean, default=False)

    exams = relationship("Exam", back_populates="subject")


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)

    study_hours = Column(Float)
    avg_grade = Column(Float)
    attendance_rate = Column(Float)
    completed_works = Column(Float)
    passed = Column(Boolean)

    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="exams")
