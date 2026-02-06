🎓 Academic Burnout Prediction System

End-to-End Machine Learning & MLOps Project

📌 Project Overview

The Academic Burnout Prediction System is an end-to-end machine learning application designed to predict student burnout risk based on behavioral and engagement metrics.
The project follows real-world MLOps practices, covering model training, evaluation, inference API development, data persistence, visualization, and cloud deployment.

This system helps educational institutions identify at-risk students early and take preventive actions.

🧠 Problem Statement

Academic burnout is often caused by:

Prolonged inactivity

Late submissions

Reduced engagement

Irregular learning patterns

Manual identification is difficult and error-prone.
This project automates burnout risk detection using machine learning + analytics dashboards.

🏗️ System Architecture
Student Activity Data
        ↓
ML Model (Scikit-Learn)
        ↓
FastAPI Inference Service
        ↓
SQLite Database (Predictions)
        ↓
Streamlit Dashboard (Charts & Trends)

⚙️ Tech Stack
🔹 Machine Learning

Python

Scikit-Learn

NumPy

Pandas

Imbalanced data handling

Probabilistic classification

🔹 MLOps & Backend

FastAPI (Inference API)

Joblib (Model serialization)

SQLite (Prediction storage)

SQLAlchemy (ORM)

Alembic (DB migrations)

🔹 Experiment Tracking

MLflow (training & evaluation phase only)

🔹 Visualization

Streamlit

Interactive charts & trends

🔹 Deployment

FastAPI → Render

Streamlit Dashboard → Streamlit Cloud

📊 Features

✔ Predict burnout probability
✔ Binary burnout classification
✔ Store predictions in database
✔ Visualize trends and statistics
✔ Modular & scalable project structure
✔ Cloud-ready deployment

📂 Project Structure
end-to-end-mlops-academic-burnout/
│
├── src/
│   ├── serving/
│   │   ├── app.py              # FastAPI app
│   │   ├── model.pkl           # Trained ML model
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── crud.py
│   │
│   ├── schema/
│   │   └── student_activity.py
│
├── streamlit_dashboard.py
├── requirements.txt
├── README.md

🔌 API Usage
Health Check
GET /

Predict Burnout
POST /predict

Request Body
{
  "login_count": 0,
  "avg_session_duration_min": 5,
  "inactive_days_streak": 15,
  "forum_posts": 0,
  "resources_accessed": 0,
  "assignments_due": 5,
  "assignments_submitted": 0,
  "submission_delay_hours": 48,
  "late_submission_ratio_7d": 1,
  "late_night_activity_ratio": 0.9,
  "weekend_activity_ratio": 0.8,
  "engagement_drop_pct_14d": 0.9,
  "consistency_score": 0.1
}

Response
{
  "burnout_probability": 0.725,
  "burnout_prediction": 1
}

📈 Streamlit Dashboard

The Streamlit dashboard provides:

Burnout probability distribution

Prediction history

Trend analysis

Interactive analytics

🚀 Deployment
FastAPI (Render)

Production inference API

Auto-scaling enabled

Streamlit (Streamlit Cloud)

Public dashboard access

Real-time visualizations

🧪 Model Details

Classification model trained with imbalance handling

Outputs probability + binary prediction

Threshold-based classification (≥ 0.5 → Burnout)

🎯 Learning Outcomes

End-to-end ML pipeline design
Practical MLOps workflow
Model serving in production
Cloud deployment
Data visualization for ML insights

📌 Author

Shaik Nabi Mansoor
Machine Learning & MLOps Enthusiast