from sqlalchemy.orm import Session
from .models import Prediction

def save_prediction(db: Session, data: dict, prob: float, pred: int):
    record = Prediction(
        **data,
        burnout_probability=prob,
        burnout_prediction=pred
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
