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

#Route POST pour ajouter une entrées dans Classe
@router.post("/classe/", response_model = schemas.ClasseResponse)
def postClasse(classe: schemas.ClasseCreate, db: Session = Depends(get_db)):
    db_classe = models.Classe(**classe.dict())
    db.add(db_classe)
    db.commit()
    db.refresh(db_classe)

    return db_classe