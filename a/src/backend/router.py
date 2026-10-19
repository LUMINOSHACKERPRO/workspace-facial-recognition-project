from fastapi import HTTPException, Depends, APIRouter, status, Query
import schemas
import models
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/faces",
    tags=["faces"]
)



@router.post("/", response_model=schemas.FaceResponse)
def enroll_face(face: schemas.EnrollFace, db: Session = Depends(get_db)):