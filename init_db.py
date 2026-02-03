from src.db.database import engine
from src.db.models import Base

Base.metadata.create_all(bind=engine)

print("✅ Database initialized")
