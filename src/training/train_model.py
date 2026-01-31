import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.utils import resample

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "student_activity_processed.csv")

# Load data
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

TARGET_COL = "burnout_flag"

X = df[FEATURES]
y = df[TARGET_COL]

print("FULL DATASET LABELS")
print(y.value_counts())

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Upsample minority class
train_data = pd.concat([X_train, y_train], axis=1)
majority = train_data[train_data[TARGET_COL] == 0]
minority = train_data[train_data[TARGET_COL] == 1]

minority_upsampled = resample(
    minority,
    replace=True,
    n_samples=len(majority),
    random_state=42
)

train_balanced = pd.concat([majority, minority_upsampled])

X_train_bal = train_balanced[FEATURES]
y_train_bal = train_balanced[TARGET_COL]

# MLflow
mlflow.set_experiment("academic_burnout_prediction")

with mlflow.start_run():
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42
    )

    model.fit(X_train_bal, y_train_bal)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    mlflow.log_params({
        "model_type": "RandomForest",
        "n_estimators": 100,
        "max_depth": 6
    })

    mlflow.log_metrics({
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob)
    })

    mlflow.sklearn.log_model(model, "model")

print("Training complete. Metrics logged to MLflow.")
