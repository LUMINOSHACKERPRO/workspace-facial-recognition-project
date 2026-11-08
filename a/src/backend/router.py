from fastapi import HTTPException, Depends, APIRouter, status, Query
from functools import lru_cache
import schemas
import models
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import List


from FaceRecogEngine import FaceRecognitionEngine

router = APIRouter(
    prefix="/faces",
    tags=["faces"]
)

#Cache the engine to improve load time 
@lru_cache()
def get_engine():
    return FaceRecognitionEngine()


#Work in progress
@router.post("/", response_model=schemas.EmbeddingResponse)
def enroll_face(face: schemas.EnrollPerson, db: Session = Depends(get_db)):
    engine = get_engine()
    
    try:
        embedding_list = engine.embed(face.base64_face_img)

        if embedding_list is None:
            raise HTTPException(status_code=422, detail="No face detected in the image")

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    new_person = models.Person(
        name = face.name,
    )

    db.add(new_person)
    db.flush()

    new_embedding = models.Embedding(
        embedding = embedding_list,
        person_id = new_person.id
    )


    db.add(new_embedding)
    try:
        db.commit()
        db.refresh(new_embedding)
    except Exception as e:
        db.rollback()
        print(f"Error saving to database: {e}")
        raise HTTPException(status_code=409 ,detail="Could not reach database...")
    
    return new_embedding


@router.get("/recognizeFace", response_model=schemas.PersonResponse)
def recognize_face(base64_string: str, db: Session = Depends(get_db)): 
    engine = get_engine()

    try:
        embedding_list = engine.embed(base64_string)

        if embedding_list is None:
            raise HTTPException(status_code=422, detail="No face detected in the image")

        distance = models.Embedding.embedding.l2_distance(embedding_list)

    except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    person = models.Person
    embedding = models.Embedding

    row = db.execute(
                    select(person.id, person.name, distance.label("distance"))
                    .select_from(embedding)
                    .join(person, person.id == embedding.person_id)
                    .order_by(distance)
                    .limit(1)
                    ).first()

    RECOGNITION_THRESHOLD = 0.9
    response = schemas.PersonResponse

    if row is None:
        return response(id=None, name="Unknown")
    if row.distance > RECOGNITION_THRESHOLD:
        return response(id=None, name="Unknown Metrics")

    return response(id=row.id, name= row.name)

@router.post("/getPeople", response_model=List[schemas.PersonResponse])
def get_people(db: Session = Depends(get_db)):

    return db.query(models.Person).order_by(models.Person.name.desc()).all()
