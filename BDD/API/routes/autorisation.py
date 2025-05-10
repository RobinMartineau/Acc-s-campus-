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
@router.post("/autorisation/",
    summary="Créer une autorisation",
    description="Cette route permet de créer une autorisation pour un utilisateur dans une salle. "
                "L'autorisation précise si l'utilisateur est autorisé ou non à accéder à la salle.",
    response_model=schemas.Autorisation,
    responses={
        201: {
            "description": "Autorisation créée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "id_utilisateur": 3,
                        "id_salle": 2,
                        "autorisee": True
                    }
                }
            }
        },
        400: {
            "description": "Erreur de validation des données (données manquantes ou incorrectes)",
            "content": {
                "application/json": {
                    "example": {"detail": "Données invalides"}
                }
            }
        }
    },
tags=["PGS"])
def postAutorisation(autorisation: schemas.AutorisationCreate, db: Session = Depends(get_db)):
    db_autorisation = models.Autorisation(**autorisation.dict())
    db.add(db_autorisation)
    db.commit()
    db.refresh(db_autorisation)

    return db_autorisation

@router.delete("/autorisation/{id}",
    summary="Supprimer une autorisation",
    description="Cette route permet de supprimer une autorisation existante en fonction de son identifiant.",
    responses={
        204: {
            "description": "Autorisation supprimée avec succès"
        },
        404: {
            "description": "Autorisation introuvable",
            "content": {
                "application/json": {
                    "example": {"detail": "Autorisation introuvable"}
                }
            }
        }
    },
tags=["PGS"])
def delete_autorisation(id_autorisation: int, db: Session = Depends(get_db)):
    autorisation = db.query(models.Autorisation).filter(models.Autorisation.id == id_autorisation).first()
    if not autorisation:
        raise HTTPException(status_code=404, detail="Autorisation non trouvée")
    
    db.delete(autorisation)
    db.commit()
    return {"detail": "Autorisation supprimée"}
