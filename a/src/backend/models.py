from database import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

class Person(Base):
    __tablename__ = "People"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

class Embedding(Base):
    __tablename__ = "Face_Embeddings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    embedding = mapped_column(Vector(512))
    person_id: Mapped[int] = mapped_column(ForeignKey("People.id"))
