# ml/predict.py
import os
import numpy as np
from sqlalchemy.orm import Session
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

from database.models import Subject

# Те же пути, что и в train.py, чтобы найти файлы модели
SAVED_MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(SAVED_MODEL_DIR, "my_model.h5")
SCALER_MEAN_PATH = os.path.join(SAVED_MODEL_DIR, "scaler_mean.npy")
SCALER_SCALE_PATH = os.path.join(SAVED_MODEL_DIR, "scaler_scale.npy")

def load_model_and_scaler():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Модель не найдена. Сперва обучите модель (POST /train).")

    model = load_model(MODEL_PATH)

    mean_ = np.load(SCALER_MEAN_PATH)
    scale_ = np.load(SCALER_SCALE_PATH)

    scaler = StandardScaler()
    scaler.mean_ = mean_
    scaler.scale_ = scale_
    scaler.var_ = scaler.scale_ ** 2

    return model, scaler

def predict_chance(db: Session, data):

    model, scaler = load_model_and_scaler()

    subj = db.query(Subject).filter(Subject.id == data.subject_id).first()
    if not subj:
        raise ValueError(f"Subject with id={data.subject_id} not found.")

    is_hard = 1 if subj.is_hard else 0

    features = np.array([[
        data.study_hours,
        data.avg_grade,
        data.attendance_rate,
        data.completed_works,
        data.subject_id,
        is_hard
    ]], dtype=float)

    features_scaled = scaler.transform(features)
    pred = model.predict(features_scaled)
    probability = float(pred[0][0])
    return probability

def delete_saved_model_files() -> list[str]:

    deleted = []
    files = [MODEL_PATH, SCALER_MEAN_PATH, SCALER_SCALE_PATH]
    for f in files:
        if os.path.exists(f):
            os.remove(f)
            deleted.append(f)
    return deleted
