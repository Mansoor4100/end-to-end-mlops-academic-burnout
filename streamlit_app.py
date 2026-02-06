import streamlit as st
import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
API_URL = "http://localhost:8000/predict"   # change after deployment
DB_PATH = "burnout.db"

st.set_page_config(
    page_title="Academic Burnout Dashboard",
    layout="wide"
)

st.title("📊 Academic Burnout Prediction Dashboard")

# =========================
# DATABASE FUNCTIONS
# =========================
def get_predictions():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY created_at DESC",
        conn
    )
    conn.close()
    return df


# =========================
# SIDEBAR - INPUT FORM
# =========================
st.sidebar.header("🎯 Student Activity Input")

with st.sidebar.form("prediction_form"):
    login_count = st.number_input("Login Count", 0, 100, 10)
    avg_session_duration_min = st.number_input("Avg Session Duration (min)", 0.0, 300.0, 30.0)
    inactive_days_streak = st.number_input("Inactive Days Streak", 0, 60, 3)
    forum_posts = st.number_input("Forum Posts", 0, 50, 1)
    resources_accessed = st.number_input("Resources Accessed", 0, 200, 20)
    assignments_due = st.number_input("Assignments Due", 0, 20, 2)
    assignments_submitted = st.number_input("Assignments Submitted", 0, 20, 1)
    submission_delay_hours = st.number_input("Submission Delay (hrs)", 0.0, 200.0, 5.0)
    late_submission_ratio_7d = st.slider("Late Submission Ratio (7d)", 0.0, 1.0, 0.2)
    late_night_activity_ratio = st.slider("Late Night Activity Ratio", 0.0, 1.0, 0.3)
    weekend_activity_ratio = st.slider("Weekend Activity Ratio", 0.0, 1.0, 0.4)
    engagement_drop_pct_14d = st.slider("Engagement Drop % (14d)", 0.0, 100.0, 15.0)
    consistency_score = st.slider("Consistency Score", 0.0, 1.0, 0.7)

    submit = st.form_submit_button("🔍 Predict Burnout")


# =========================
# PREDICTION CALL
# =========================
if submit:
    payload = {
        "login_count": login_count,
        "avg_session_duration_min": avg_session_duration_min,
        "inactive_days_streak": inactive_days_streak,
        "forum_posts": forum_posts,
        "resources_accessed": resources_accessed,
        "assignments_due": assignments_due,
        "assignments_submitted": assignments_submitted,
        "submission_delay_hours": submission_delay_hours,
        "late_submission_ratio_7d": late_submission_ratio_7d,
        "late_night_activity_ratio": late_night_activity_ratio,
        "weekend_activity_ratio": weekend_activity_ratio,
        "engagement_drop_pct_14d": engagement_drop_pct_14d,
        "consistency_score": consistency_score
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        prob = result["burnout_probability"]
        pred = result["burnout_prediction"]

        st.subheader("📌 Prediction Result")

        if pred == 1:
            st.error(f"⚠️ High Burnout Risk (Probability: {prob})")
        else:
            st.success(f"✅ Low Burnout Risk (Probability: {prob})")
    else:
        st.error("Prediction API failed")


# =========================
# DASHBOARD ANALYTICS
# =========================
st.divider()
st.header("📈 Burnout Analytics")

df = get_predictions()

if df.empty:
    st.info("No predictions available yet.")
else:
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Predictions",
        len(df)
    )

    col2.metric(
        "High Risk %",
        f"{(df['burnout_prediction'].mean() * 100):.1f}%"
    )

    col3.metric(
        "Avg Burnout Probability",
        f"{df['burnout_probability'].mean():.2f}"
    )

    # =========================
    # CHARTS
    # =========================
    st.subheader("📊 Charts")

    colA, colB = st.columns(2)

    # Burnout Probability Distribution
    with colA:
        fig, ax = plt.subplots()
        ax.hist(df["burnout_probability"], bins=10)
        ax.set_title("Burnout Probability Distribution")
        ax.set_xlabel("Probability")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    # Burnout Count
    with colB:
        counts = df["burnout_prediction"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(["No Burnout", "Burnout"], counts.reindex([0, 1], fill_value=0))
        ax.set_title("Burnout vs Non-Burnout")
        st.pyplot(fig)

    # Trend Over Time
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"])
        trend = df.sort_values("created_at")

        st.subheader("📉 Burnout Trend Over Time")
        fig, ax = plt.subplots()
        ax.plot(trend["created_at"], trend["burnout_probability"])
        ax.set_ylabel("Burnout Probability")
        ax.set_xlabel("Time")
        st.pyplot(fig)
