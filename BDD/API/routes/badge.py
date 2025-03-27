from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
import datetime

#Instanciation d'un router FastAPI
router = APIRouter()

#Fonction pour récupérer la session de la BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Route POST pour ajouter une entrées dans Badge_RFID
@router.post("/badge/", response_model = schemas.BadgeResponse)
def postBadge(badge: schemas.BadgeCreate, db: Session = Depends(get_db)):
    date_actuelle = datetime.date.today()

    db_badge = models.Badge(
        uid = badge.uid,
        actif = badge.actif,
        creation = date_actuelle,
        id_utilisateur = badge.id_utilisateur
    )

    db.add(db_badge)
    db.commit()
    db.refresh(db_badge)
    
    return db_badge
