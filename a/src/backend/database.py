from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'postgresql://postgres:test1234@localhost:5432/face_recognition_webapp'

Base = declarative_base()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, 
                       autoflush=False, 
                       bind=engine)


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

