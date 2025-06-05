
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use environment variables for database credentials in a real application
# For this assignment, we'll use a default local setup
# Assumes PostgreSQL is running locally or in Docker with default user/pass/db
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tradedb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

