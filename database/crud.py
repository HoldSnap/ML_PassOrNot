from sqlalchemy.orm import Session
from .models import Subject, Exam
from .schemas import SubjectCreate, ExamCreate

def create_subject(db: Session, subject_data: SubjectCreate):
    existing = db.query(Subject).filter(Subject.name == subject_data.name).first()
    if existing:
        return None  # Или выбрасываем ошибку выше
    new_subj = Subject(name=subject_data.name, is_hard=subject_data.is_hard)
    db.add(new_subj)
    db.commit()
    db.refresh(new_subj)
    return new_subj

def get_subjects(db: Session):
    return db.query(Subject).all()

def create_exam(db: Session, exam_data: ExamCreate):
    subj = db.query(Subject).filter(Subject.id == exam_data.subject_id).first()
    if not subj:
        return None
    new_exam = Exam(
        student_name=exam_data.student_name,
        study_hours=exam_data.study_hours,
        avg_grade=exam_data.avg_grade,
        attendance_rate=exam_data.attendance_rate,
        completed_works=exam_data.completed_works,
        passed=exam_data.passed,
        subject_id=exam_data.subject_id
    )
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return new_exam

def get_exams(db: Session):
    return db.query(Exam).all()
