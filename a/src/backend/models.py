from database import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String

class Face(Base):
    __tablename__ = "Faces"

    person_name = Column(String, primary_key=True, index=True)
    embedding = Column(Vector(512), nullable=True)
