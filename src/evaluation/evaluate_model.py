import os
import pandas as pd
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

# ---------------- PATHS ----------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "student_activity_processed.csv"
)

MODEL_URI = "runs:/c3c34880bde24306a3a9d87436d985e8/model"

TARGET_COL = "burnout_flag"

FEATURES = [
    "login_count",
    "avg_session_duration_min",
    "inactive_days_streak",
    "forum_posts",
    "resources_accessed",
    "assignments_due",
    "assignments_submitted",
    "submission_delay_hours",
    "late_submission_ratio_7d",
    "late_night_activity_ratio",
    "weekend_activity_ratio",
    "engagement_drop_pct_14d",
    "consistency_score"
]

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATA_PATH)

X = df[FEATURES]   # ✅ FIX: same features as training
y = df[TARGET_COL]

# ---------------- LOAD MODEL ----------------
model = mlflow.sklearn.load_model(MODEL_URI)

# ---------------- PREDICTION ----------------
y_pred = model.predict(X)

# ---------------- METRICS ----------------
print("\nClassification Report:\n")
print(classification_report(y, y_pred))

cm = confusion_matrix(y, y_pred)

# ---------------- PLOT ----------------
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
