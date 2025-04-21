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

#Route POST pour ajouter une entrées dans Salle
@router.post("/salle/", response_model = schemas.SalleResponse, include_in_schema=False)
def postSalle(salle: schemas.SalleCreate, db: Session = Depends(get_db)):
    db_salle = models.Salle(**salle.dict())
    db.add(db_salle)
    db.commit()
    db.refresh(db_salle)

    return db_salle