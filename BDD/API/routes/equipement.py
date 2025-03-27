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

#route POST pour ajouter une nouvelle entrée dans Equipement
@router.post("/equipement/", response_model = schemas.EquipementResponse)
def postEquipement(equipement: schemas.EquipementCreate, db: Session = Depends(get_db)):
    db_equipement = models.Equipement(**equipement.dict())
    db.add(db_equipement)
    db.commit()
    db.refresh(db_equipement)

    return db_equipement