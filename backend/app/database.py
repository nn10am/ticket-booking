from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from .config import settings 

# Create SQLAlchemy engine 
engine = create_engine(settings.DATABASE_URL) 

# Create a configured "Session" class 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Create a base class 
Base = declarative_base() 

# Dependency to get the database session 
def get_db(): 
    try:
        db = SessionLocal() 
        yield db 
    finally: 
        db.close()