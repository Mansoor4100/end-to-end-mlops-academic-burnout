import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "student_activity_raw.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

df = pd.read_csv(RAW_PATH)
df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(["student_id", "date"])

df["login_7d_avg"] = (
    df.groupby("student_id")["login_count"]
    .rolling(7)
    .mean()
    .reset_index(0, drop=True)
)

df["login_14d_avg"] = (
    df.groupby("student_id")["login_count"]
    .rolling(14)
    .mean()
    .reset_index(0, drop=True)
)

df["engagement_drop_pct_14d"] = (
    (df["login_7d_avg"] - df["login_14d_avg"]) /
    (df["login_14d_avg"] + 1e-5)
)
df["late_submission_flag"] = (df["submission_delay_hours"] > 24).astype(int)

df["late_submission_ratio_7d"] = (
    df.groupby("student_id")["late_submission_flag"]
    .rolling(7)
    .mean()
    .reset_index(0, drop=True)
)

conditions_high = (
    (df["engagement_drop_pct_14d"] < -0.4) &
    (df["late_submission_ratio_7d"] > 0.4)
)

conditions_medium = (
    (df["engagement_drop_pct_14d"] < -0.2)
)

df["burnout_risk_label"] = "low"
df.loc[conditions_medium, "burnout_risk_label"] = "medium"
df.loc[conditions_high, "burnout_risk_label"] = "high"

df["burnout_flag"] = (df["burnout_risk_label"] == "high").astype(int)

df = df.dropna().reset_index(drop=True)
output_path = os.path.join(PROCESSED_DIR, "student_activity_processed.csv")
df.to_csv(output_path, index=False)
print(df["burnout_risk_label"].value_counts())
