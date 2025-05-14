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

#Route GET pour récupérer toutes les salles
@router.get("/salle/",
    response_model = list[schemas.SalleResponse],
    summary="Récupérer la liste des salles",
    description="Cette route permet d'obtenir la liste complète des salles enregistrées dans la base de données avec leur numéro, digicode et statut.",
    responses={
        200: {
            "description": "Salles récupérées avec succès",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "numero": "B101",
                            "statut": True
                        },
                        {
                            "id": 2,
                            "numero": "C302",
                            "statut": False
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Salles non trouvées",
            "content": {
                "application/json": {
                    "example": {"detail": "Salles non trouvées"}
                }
            }
        }
    },
tags=["PSW", "PGS"])
def getSalles(db: Session = Depends(get_db)):
    salle = db.query(models.Salle).all()
    
    if not salle:
        raise HTTPException(status_code = 404, detail = "Salles non trouvées")    
    
    return salle

#Route GET pour récupérer l'id d'une salle en fonction du numéro
@router.get(
    "/salle/{numero}",
    summary="Obtenir l'ID d'une salle via son numéro",
    description=(
        "Permet de récupérer l'identifiant unique (`id`) d'une salle à partir de son numéro (ex. : 'A101').\n\n"
        "Ce `id` est utilisé dans d'autres opérations comme l'enregistrement d'un équipement ou une réservation."
    ),
    responses={
        200: {
            "description": "Identifiant de salle récupéré avec succès",
            "content": {
                "application/json": {
                    "example": 5
                }
            }
        },
        404: {
            "description": "Salle non trouvée",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Salle non trouvée"
                    }
                }
            }
        }
    },
tags=["PEA", "BAE"])
def getIdSalle(numero: str, db: Session = Depends(get_db)):
    salle = db.query(models.Salle).filter(models.Salle.numero == numero).first()

    if not salle:
        raise HTTPException(status_code = 404, detail = "Salle non trouvée")

    return salle.id
