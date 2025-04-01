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

#Route GET pour récupérer toutes les entrées dans Badge
@router.get("/badge/", response_model = list[schemas.BadgeResponse], include_in_schema = False)
def getBadges(db: Session = Depends(get_db)):

    return db.query(models.Badge).all()
        
#Route GET pour récupérer l'entrée correspondant à  l'uid dans Badge
@router.get("/badge/{uid}", response_model = schemas.BadgeResponse, include_in_schema = False)
def getBadge(uid: int, db: Session = Depends(get_db)):
    badge = db.query(models.Badge).filter(models.Badge.id == id_badge).first()

    if not badge:
        raise HTTPException(status_code = 404, detail = "Badge non trouvé")

    return badge

#Route POST pour ajouter une entrées dans Badge
@router.post("/badge/",
    summary="Créer un nouveau badge",
    description="Cette route permet d'ajouter un badge à la base de données et de l'associer à un utilisateur.",
    responses={
        200: {
            "description": "Badge créé avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "uid": "A1B2C3D4F6",
                        "actif": True,
                        "creation": "2025-03-31"
                    }
                }
            }
        },
        400: {
            "description": "Erreur de validation",
            "content": {
                "application/json": {
                    "examples": {
                        "UID déjà existant": {
                            "summary": "Un badge avec cet UID est déjà enregistré",
                            "value": {"detail": "Badge déjà enregistré"}
                        },
                        "Utilisateur introuvable": {
                            "summary": "L'ID de l'utilisateur ne correspond à aucun compte",
                            "value": {"detail": "Utilisateur introuvable"}
                        }
                    }
                }
            }
        }
    }
)
def postBadge(badge: schemas.BadgeCreate, db: Session = Depends(get_db)):
    date_actuelle = datetime.date.today()

    #Vérifier si le badge avec cet UID existe déjà
    existant = db.query(models.Badge).filter(models.Badge.uid == badge.uid).first()

    if existant:
        raise HTTPException(status_code=400, detail="Badge déjà enregistré")

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
    
#Route DELETE pour supprimer l'entrée correspondant à l'uid dans Badge
@router.delete("/badge/{uid}", include_in_schema = False)
def deleteBadge(uid: int, db: Session = Depends(get_db)):
    badge = db.query(models.Badge).filter(models.Badge.uid == uid).first()

    if not badge:
        raise HTTPException(status_code = 404, detail = "Badge non trouvé")

    db.delete(badge)
    db.commit()

    return
