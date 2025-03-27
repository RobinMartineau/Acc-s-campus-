from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas

#Instanciation d'un router FastAPI
router = APIRouter()

#Fonction pour récupérer la session de la BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Route POST pour ajouter une entrées dans Salle
@router.post("/salle/", response_model = schemas.SalleResponse)
def postSalle(salle: schemas.SalleCreate, db: Session = Depends(get_db)):
    db_salle = models.Salle(**salle.dict())
    db.add(db_salle)
    db.commit()
    db.refresh(db_salle)

    return db_salle