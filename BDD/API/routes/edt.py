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

#Route POST pour ajouter une entrée dans EDTUtilisateur    
@router.post("/creneau/utilisateur/", response_model = schemas.EDTUtilisateurResponse, include_in_schema=False)
def postEDTUtilisateur(creneau: schemas.EDTUtilisateurCreate, db: Session = Depends(get_db)):
    db_creneau = models.EDTUtilisateur(**creneau.dict())
    db.add(db_creneau)
    db.commit()
    db.refresh(db_creneau)

    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == db_creneau.id_utilisateur,).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur non trouvé")

    #Création d'une entrée absence pour les élèves seulement
    if utilisateur.role == "Eleve":
        absence_entry = models.Absence(
            id_edtutilisateur = db_creneau.id,
            id_utilisateur = utilisateur.id,
            valide = True
        )
        db.add(absence_entry)
        db.commit()
        db.refresh(absence_entry)
    
    return db_creneau