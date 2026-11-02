from fastapi import HTTPException, Depends, APIRouter, status, Query
from functools import lru_cache
import schemas
import models
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from FaceRecogEngine import FaceRecognitionEngine

router = APIRouter(
    prefix="/faces",
    tags=["faces"]
)

@lru_cache()
def get_engine():
    return FaceRecognitionEngine()


#Work in progress
@router.post("/", response_model=schemas.FaceResponse)
def enroll_face(face: schemas.EnrollFace, db: Session = Depends(get_db)):
    engine = get_engine()
    
    try:
        raw_embedding = engine.embed(face.base64)
        # Convert numpy array or Vector to standard list
        embedding_list = raw_embedding.tolist() if hasattr(raw_embedding, "tolist") else list(raw_embedding) #FIXME: fix the pylance attribute error on .tolist()!
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    new_face = models.Face(
        person_name = face.name,
        embedding = embedding_list
    )

    db.add(new_face)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error saving to database: {e}")
        raise HTTPException(status_code=409 ,detail="Could not reach database...")
    
    db.refresh(new_face)
    return new_face
    
