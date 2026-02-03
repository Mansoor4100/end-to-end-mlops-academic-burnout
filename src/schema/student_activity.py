from pydantic import BaseModel

class StudentActivity(BaseModel):
    login_count: int
    avg_session_duration_min: float
    inactive_days_streak: int
    forum_posts: int
    resources_accessed: int
    assignments_due: int
    assignments_submitted: int
    submission_delay_hours: float
    late_submission_ratio_7d: float
    late_night_activity_ratio: float
    weekend_activity_ratio: float
    engagement_drop_pct_14d: float
    consistency_score: float
