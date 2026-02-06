
import os
import mlflow
import mlflow.sklearn
import numpy as np
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import joblib
import mlflow.sklearn
from src.db.database import SessionLocal
from src.db.crud import save_prediction
from src.schema.student_activity import StudentActivity  # ✅ correct import

app = FastAPI(
    title="Academic Burnout Prediction API",
    version="1.0"
)



MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(MODEL_PATH)



# -------------------------
# DB Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "API is running"}


@app.post("/predict")
def predict(
    data: StudentActivity,
    db: Session = Depends(get_db)   # ✅ ONLY addition
):
    X = np.array([[ 
        data.login_count,
        data.avg_session_duration_min,
        data.inactive_days_streak,
        data.forum_posts,
        data.resources_accessed,
        data.assignments_due,
        data.assignments_submitted,
        data.submission_delay_hours,
        data.late_submission_ratio_7d,
        data.late_night_activity_ratio,
        data.weekend_activity_ratio,
        data.engagement_drop_pct_14d,
        data.consistency_score
    ]])

    prob = model.predict_proba(X)[0][1]
    prediction = int(prob >= 0.5)

    # -------------------------
    # SAVE TO DATABASE ✅
    # -------------------------
    save_prediction(
        db=db,
        data=data.dict(),
        prob=float(prob),
        pred=prediction
    )

    return {
        "burnout_probability": round(float(prob), 3),
        "burnout_prediction": prediction
    }
