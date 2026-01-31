import os
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "student_activity_processed.csv")

df = pd.read_csv(DATA_PATH)
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

X = df[FEATURES]
y = df["burnout_flag"]
print("FULL DATASET LABELS")
print(y.value_counts())
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
mlflow.set_experiment("academic_burnout_prediction")

with mlflow.start_run():
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)

if y_prob.shape[1] == 2:
    y_prob = y_prob[:, 1]
else:
    raise ValueError("Model trained with single class. Check target labels.")

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)
mlflow.log_params({
    "model_type": "RandomForest",
    "n_estimators": 100,
    "max_depth": 6
})

mlflow.log_metrics({
    "accuracy": acc,
    "f1_score": f1,
    "roc_auc": auc
})

mlflow.sklearn.log_model(model, "model")
print(y_train.value_counts())

