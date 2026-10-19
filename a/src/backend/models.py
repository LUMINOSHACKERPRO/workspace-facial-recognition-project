from database import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String

class person(Base):
    __tablename__ = "Faces"

    name = Column(String, primary_key=True, index=True)
    embedding = Column(Vector(512), nullable=False)