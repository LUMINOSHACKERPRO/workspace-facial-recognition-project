from pydantic import BaseModel
from pgvector.sqlalchemy import Vector

# Data sent from the app (name and image) to FastAPI
class EnrollFace(BaseModel):
    name: str
    base64: str

# Data that will be sent to the database
class FaceResponse(BaseModel):
    name: str
    embedding: list[float]

    class Config:
        from_attributes = True
