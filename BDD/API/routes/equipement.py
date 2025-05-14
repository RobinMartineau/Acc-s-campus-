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
@router.post(
    "/equipement/",
    response_model=schemas.EquipementResponse,
    summary="Ajouter un équipement",
    description=(
        "Ajoute un nouvel équipement (PEA ou BAE) en base de données. "
        "L'adresse MAC doit être unique, sinon un code 409 est renvoyé.\n\n"
        "Cette route est utilisée lors de l'enregistrement automatique d'un appareil au premier démarrage."
    ),
    responses={
        201: {
            "description": "Équipement ajouté avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "id": 12,
                        "adresse_mac": "aa:bb:cc:dd:ee:ff",
                        "type": "PEA",
                        "id_salle": 3
                    }
                }
            }
        },
        409: {
            "description": "Adresse MAC déjà enregistrée",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Conflit possible avec l'adresse mac."
                    }
                }
            }
        }
    },
tags=["PEA", "BAE"])
def postEquipement(equipement: schemas.EquipementCreate, db: Session = Depends(get_db)):
    equipement = db.query(models.Equipement).filter(models.Equipement.adresse_mac == equipement.adresse_mac).first()

    if equipement:
        raise HTTPException(status_code = 409, detail = "Conflit possible avec l'adresse mac.")
    
    db_equipement = models.Equipement(**equipement.dict())
    db.add(db_equipement)
    db.commit()
    db.refresh(db_equipement)

    return db_equipement

#Route DELETE pour supprimer l'entrée correspondant à l'id dans Equipement
@router.delete(
    "/equipement/{id_equipement}",
    summary="Supprimer un équipement",
    description=(
        "Supprime un équipement (PEA ou BAE) identifié par son ID. "
        "Si aucun équipement ne correspond, renvoie une erreur 404.\n\n"
        "Cette suppression entraîne aussi la suppression en cascade des logs liés."
    ),
    responses={
        204: {
            "description": "Équipement supprimé avec succès (aucun contenu retourné)"
        },
        404: {
            "description": "Aucun équipement trouvé pour cet ID",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Equipement non trouvée"
                    }
                }
            }
        }
    },
tags=["PEA", "BAE"])
def deleteEquipement(id_equipement: int, db: Session = Depends(get_db)):
    equipement = db.query(models.Equipement).filter(models.Equipement.id == id_equipement).first()

    if not equipement:
        raise HTTPException(status_code=404, detail="Equipement non trouvée")

    db.delete(equipement)
    db.commit()
    return