from pydantic import BaseModel
from pgvector.sqlalchemy import Vector
from typing import Optional

# Data sent from the app (name and image) to FastAPI
class EnrollPerson(BaseModel):
    name: str
    base64_face_img: str

# Data that will be sent to the frontend after successfully enrolling a person
class EmbeddingResponse(BaseModel):
    id: int
    embedding: list[float]
    person_id: int

    class Config:
        from_attributes = True

# Data from the people enrolled that will be sent to the frontend
class PersonResponse(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True
