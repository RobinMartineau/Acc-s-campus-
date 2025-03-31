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

#Route POST pour ajouter une entrées dans Badge
@router.post("/badge/",
    summary="Créer un nouveau badge",
    description="Cette route permet d'ajouter un badge à la base de données et de l'associer à un utilisateur.",
    responses={
        201: {
            "description": "Badge créé avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "id": 25,
                        "uid": "A1B2C3D4F6",
                        "actif": True,
                        "creation": "2025-03-31",
                        "id_utilisateur": 12
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

    #Vérifier que l'utilisateur existe
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == badge.id_utilisateur).first()

    if not utilisateur:
        raise HTTPException(status_code=400, detail="Utilisateur introuvable")

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
