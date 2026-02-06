from src.db.database import Base, engine
from src.db import models  # VERY IMPORTANT: imports models

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done ✅")
