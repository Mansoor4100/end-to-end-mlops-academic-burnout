import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Academic Burnout Predictor", layout="centered")

st.title("🎓 Academic Burnout Prediction System")
st.write("Enter student engagement details to assess burnout risk.")

# Input fields
login_count = st.number_input("Login Count", 0, 100, 0)
avg_session_duration_min = st.number_input("Avg Session Duration (min)", 0, 300, 0)
inactive_days_streak = st.number_input("Inactive Days Streak", 0, 60, 0)
forum_posts = st.number_input("Forum Posts", 0, 100, 0)
resources_accessed = st.number_input("Resources Accessed", 0, 200, 0)
assignments_due = st.number_input("Assignments Due", 0, 20, 0)
assignments_submitted = st.number_input("Assignments Submitted", 0, 20, 0)
submission_delay_hours = st.number_input("Submission Delay (hours)", 0, 200, 0)
late_submission_ratio_7d = st.slider("Late Submission Ratio (7d)", 0.0, 1.0, 0.0)
late_night_activity_ratio = st.slider("Late Night Activity Ratio", 0.0, 1.0, 0.0)
weekend_activity_ratio = st.slider("Weekend Activity Ratio", 0.0, 1.0, 0.0)
engagement_drop_pct_14d = st.slider("Engagement Drop % (14d)", 0.0, 1.0, 0.0)
consistency_score = st.slider("Consistency Score", 0.0, 1.0, 0.0)

if st.button("🔍 Predict Burnout Risk"):
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

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        st.success("✅ Prediction Successful")
        st.metric("Burnout Probability", f"{result['burnout_probability']:.2f}")
        st.metric("Burnout Prediction", "YES 🚨" if result["burnout_prediction"] == 1 else "NO ✅")

    except Exception as e:
        st.error(f"❌ API Error: {e}")
