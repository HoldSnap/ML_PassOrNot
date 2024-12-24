

import os
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from database.crud import (
    create_subject, get_subjects,
    create_exam, get_exams
)
from database.schemas import (
    SubjectCreate, SubjectOut,
    ExamCreate, ExamOut,
    PredictRequest
)
from utils.generator import generate_data
from ml.train import get_data_for_training, train_model
from ml.predict import predict_chance, delete_saved_model_files

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Exam Passing Probability API")



@app.post("/subjects", response_model=SubjectOut, tags=["subjects"])
def api_create_subject(subj: SubjectCreate):

    db = SessionLocal()
    try:
        created = create_subject(db, subj)
        if created is None:
            raise HTTPException(status_code=400, detail="Subject with the same name already exists.")
        return created
    finally:
        db.close()


@app.get("/subjects", response_model=list[SubjectOut], tags=["subjects"])
def api_list_subjects():

    db = SessionLocal()
    try:
        return get_subjects(db)
    finally:
        db.close()



@app.post("/exams", response_model=ExamOut, tags=["exams"])
def api_create_exam(exam_data: ExamCreate):

    db = SessionLocal()
    try:
        created = create_exam(db, exam_data)
        if created is None:
            raise HTTPException(status_code=404, detail="Subject not found.")
        return created
    finally:
        db.close()


@app.get("/exams", response_model=list[ExamOut], tags=["exams"])
def api_list_exams():

    db = SessionLocal()
    try:
        return get_exams(db)
    finally:
        db.close()



@app.delete("/truncate_all", tags=["admin"])
def api_truncate_all():

    db = SessionLocal()
    try:
        db.execute("TRUNCATE TABLE exams RESTART IDENTITY CASCADE;")
        db.execute("TRUNCATE TABLE subjects RESTART IDENTITY CASCADE;")
        db.commit()
        return {"message": "All tables truncated."}
    finally:
        db.close()


@app.post("/generate_data", tags=["dev"])
def api_generate_data(num_subjects: int = 10, num_exams: int = 100):

    db = SessionLocal()
    try:
        generate_data(db, num_subjects, num_exams)
        return {"message": f"Generated {num_subjects} subjects and {num_exams} exams."}
    finally:
        db.close()



@app.post("/train", tags=["ml"])
def api_train():

    db = SessionLocal()
    try:
        X, y = get_data_for_training(db)
        if X is None or len(X) == 0:
            raise HTTPException(status_code=400, detail="No data for training.")
        acc = train_model(X, y)
        return {"message": f"Model trained. Accuracy ~ {acc:.3f}"}
    finally:
        db.close()


@app.delete("/delete_model", tags=["ml"])
def api_delete_model():

    deleted_files = delete_saved_model_files()
    if not deleted_files:
        raise HTTPException(status_code=404, detail="Model files not found.")
    return {"message": f"Deleted: {', '.join(deleted_files)}"}


@app.post("/predict", tags=["ml"])
def api_predict(data: PredictRequest):

    db = SessionLocal()
    try:
        prob = predict_chance(db, data)
        return {
            "student_name": data.student_name,
            "subject_id": data.subject_id,
            "chance_to_pass": prob
        }
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Model not found. Please train first.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    finally:
        db.close()
