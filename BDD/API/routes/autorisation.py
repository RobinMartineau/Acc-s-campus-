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

#Route POST pour ajouter une entrées dans Autorisation
@router.post("/autorisation/", response_model = schemas.AutorisationResponse, include_in_schema=False)
def postAutorisation(autorisation: schemas.AutorisationCreate, db: Session = Depends(get_db)):
    db_autorisation = models.Autorisation(**autorisation.dict())
    db.add(db_autorisation)
    db.commit()
    db.refresh(db_autorisation)

    return db_autorisation