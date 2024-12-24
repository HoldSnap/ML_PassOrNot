import os
import numpy as np
import pandas as pd

# scikit-learn и TensorFlow
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.callbacks import EarlyStopping

SAVED_MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(SAVED_MODEL_DIR, "my_model.h5")
SCALER_MEAN_PATH = os.path.join(SAVED_MODEL_DIR, "scaler_mean.npy")
SCALER_SCALE_PATH = os.path.join(SAVED_MODEL_DIR, "scaler_scale.npy")

os.makedirs(SAVED_MODEL_DIR, exist_ok=True)

def get_data_for_training(db):

    query = """
    SELECT e.*, s.is_hard
    FROM exams e
    JOIN subjects s ON e.subject_id = s.id
    """
    df = pd.read_sql(query, db.bind)
    if df.empty:
        return None, None

    X = df[[
        "study_hours",
        "avg_grade",
        "attendance_rate",
        "completed_works",
        "subject_id",
        "is_hard"
    ]]
    X["is_hard"] = X["is_hard"].astype(int)

    y = df["passed"].astype(int)
    return X, y

def train_model(X, y):

    # Разделяем на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Масштабируем
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # Сохраняем параметры скейлера в файлы .npy
    np.save(SCALER_MEAN_PATH, scaler.mean_)
    np.save(SCALER_SCALE_PATH, scaler.scale_)

    # Создаём Keras-модель
    model = Sequential([
        Input(shape=(X_train_scaled.shape[1],)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    es = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    model.fit(
        X_train_scaled, y_train,
        epochs=50,
        batch_size=32,
        validation_data=(X_test_scaled, y_test),
        callbacks=[es],
        verbose=0  # verbose=0, чтобы не захламлять вывод
    )

    # Оцениваем точность на тесте
    loss, acc = model.evaluate(X_test_scaled, y_test, verbose=0)

    model.save(MODEL_PATH)

    return acc
