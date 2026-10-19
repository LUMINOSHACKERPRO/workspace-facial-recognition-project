from pydantic import BaseModel
from pgvector.sqlalchemy import Vector


class EnrollFace(BaseModel):
    name: str
    embedding: Vector


class FaceResponse(BaseModel):
    name: str
    embedding: Vector

    class Config:
        from_attributes = True