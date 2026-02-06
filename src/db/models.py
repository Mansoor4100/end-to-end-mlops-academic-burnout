from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from .database import Base
from sqlalchemy import Column, Integer, String
from src.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    login_count = Column(Integer)
    avg_session_duration_min = Column(Float)
    inactive_days_streak = Column(Integer)
    forum_posts = Column(Integer)
    resources_accessed = Column(Integer)
    assignments_due = Column(Integer)
    assignments_submitted = Column(Integer)
    submission_delay_hours = Column(Float)
    late_submission_ratio_7d = Column(Float)
    late_night_activity_ratio = Column(Float)
    weekend_activity_ratio = Column(Float)
    engagement_drop_pct_14d = Column(Float)
    consistency_score = Column(Float)

    burnout_probability = Column(Float)
    burnout_prediction = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
