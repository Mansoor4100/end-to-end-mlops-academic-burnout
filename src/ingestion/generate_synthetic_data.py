import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

NUM_STUDENTS = 100
NUM_DAYS = 90
START_DATE = datetime(2025, 1, 1)

data = []

for student_id in range(1, NUM_STUDENTS + 1):
    engagement_base = np.random.randint(3, 8)

    for day in range(NUM_DAYS):
        date = START_DATE + timedelta(days=day)

        login_count = max(0, int(np.random.normal(engagement_base, 1)))
        avg_session = max(5, np.random.normal(45, 10))
        forum_posts = np.random.poisson(1)

        # ✅ Burnout logic (behavior-based)
        burnout_flag = 1 if (
            login_count <= 3 and
            avg_session < 35 and
            forum_posts == 0 and
            np.random.rand() < 0.9
        ) else 0

        data.append({
            "student_id": f"S{student_id:04d}",
            "date": date.date(),
            "week_no": day // 7 + 1,
            "semester_phase": "mid",

            "login_count": login_count,
            "avg_session_duration_min": avg_session,
            "inactive_days_streak": 0,
            "forum_posts": forum_posts,
            "resources_accessed": np.random.randint(1, 6),

            "assignments_due": np.random.randint(0, 2),
            "assignments_submitted": np.random.randint(0, 2),
            "submission_delay_hours": max(0, np.random.normal(5, 2)),
            "late_submission_ratio_7d": 0.0,
            "time_to_start_assignment_hr": np.random.normal(10, 3),

            "late_night_activity_ratio": np.random.uniform(0, 1),
            "weekend_activity_ratio": np.random.uniform(0, 1),
            "session_variance_7d": np.random.uniform(0, 1),
            "study_time_trend_7d": np.random.uniform(-1, 1),

            "engagement_drop_pct_14d": 0.0,
            "focus_decay_score": np.random.uniform(0, 1),
            "consistency_score": np.random.uniform(0, 1),

            "burnout_risk_label": "high" if burnout_flag == 1 else "low",
            "burnout_flag": burnout_flag
        })

# ✅ Ensure directory exists (important for Windows + CI)
os.makedirs("data/raw", exist_ok=True)

df = pd.DataFrame(data)
df.to_csv("data/raw/student_activity_raw.csv", index=False)

print("Dataset generated successfully")
print(df["burnout_flag"].value_counts())
