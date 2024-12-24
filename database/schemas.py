from typing import Optional
from pydantic import BaseModel

class SubjectCreate(BaseModel):
    name: str
    is_hard: bool = False

class SubjectOut(BaseModel):
    id: int
    name: str
    is_hard: bool

    class Config:
        orm_mode = True


class ExamCreate(BaseModel):
    student_name: str
    study_hours: float
    avg_grade: float
    attendance_rate: float
    completed_works: float
    passed: bool
    subject_id: int

class ExamOut(BaseModel):
    id: int
    student_name: str
    study_hours: float
    avg_grade: float
    attendance_rate: float
    completed_works: float
    passed: bool
    subject_id: int

    class Config:
        orm_mode = True


class PredictRequest(BaseModel):
    student_name: Optional[str] = None
    study_hours: float
    avg_grade: float
    attendance_rate: float
    completed_works: float
    subject_id: int
