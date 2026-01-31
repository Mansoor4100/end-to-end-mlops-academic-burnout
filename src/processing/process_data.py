import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "student_activity_raw.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
PROCESSED_PATH = os.path.join(PROCESSED_DIR, "student_activity_processed.csv")

os.makedirs(PROCESSED_DIR, exist_ok=True)

df = pd.read_csv(RAW_PATH)

# --- basic sanity cleaning ---
df["date"] = pd.to_datetime(df["date"])
df = df.dropna()

# (Optional) sort for time-series correctness
df = df.sort_values(["student_id", "date"])

df.to_csv(PROCESSED_PATH, index=False)

print("Processed data saved successfully")
print(df["burnout_flag"].value_counts())
