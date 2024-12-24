# utils/generator.py
import random
from sqlalchemy.orm import Session
from database.models import Subject, Exam

def generate_data(db: Session, num_subjects: int = 10, num_exams: int = 100):

    for i in range(1, num_subjects + 1):
        subj = Subject(
            id=i,
            name=f"Subject_{i}",
            is_hard=(i == 10)
        )
        db.merge(subj)
    db.commit()

    subject_ids = list(range(1, num_subjects + 1))
    for _ in range(num_exams):
        sub_id = random.choice(subject_ids)
        study_hours = round(random.uniform(0, 50), 2)
        avg_grade = round(random.uniform(2.0, 5.0), 2)
        attendance_rate = round(random.uniform(0.0, 1.0), 2)
        completed_works = round(random.uniform(0.0, 1.0), 2)

        pass_prob = (
            0.2
            + 0.15 * (study_hours / 50)
            + 0.25 * (avg_grade / 5)
            + 0.15 * attendance_rate
            + 0.15 * completed_works
        )
        pass_prob += random.uniform(-0.1, 0.1)

        if sub_id == 10:
            pass_prob -= 0.5

        pass_prob = max(0, min(1, pass_prob))
        passed = (random.random() < pass_prob)

        exam = Exam(
            student_name=f"Student_{random.randint(1, 500)}",
            study_hours=study_hours,
            avg_grade=avg_grade,
            attendance_rate=attendance_rate,
            completed_works=completed_works,
            passed=passed,
            subject_id=sub_id
        )
        db.add(exam)
    db.commit()
