from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
import datetime
import chiffrement

#Instanciation d'un router FastAPI
router = APIRouter()

#Fonction pour récupérer la session de la BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route POST pour la connexion
@router.post("/psw/login/")
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.identifiant == request.identifiant).first()

#Vérifier si l'utilisateur existe
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

#Vérifier le mot de passe
    mot_de_passe = chiffrement.decryptPassword(utilisateur.mot_de_passe)

    if mot_de_passe != request.mot_de_passe:
        raise {"success": False}
        
    return {
            "success": True,
            "id_utilisateur": utilisateur.id         
        }

#Route GET pour récupérer les absences vérifer d'un utilisateur
@router.get("/psw/absence/{id_utilisateur}")
def getUAbsence(id_utilisateur: int, db: Session = Depends(get_db)):  
    heure_actuelle = datetime.datetime.now()
    
#Récupération de tous les cours passé
    cours_passe = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == id_utilisateur,
        models.EDTUtilisateur.horairefin <= heure_actuelle
    ).all()

    id_cours_passe = [cours.id for cours in cours_passe]
    
#Récupération des absences liées au cours
    absences = db.query(models.Absence).filter(
        models.Absence.id_edtutilisateur.in_(id_cours_passe),
        models.Absence.valide == True
    ).all()

    if not absences:
        raise HTTPException(status_code = 404, detail = "Absence non trouvée")

    return [{
            "cours": cours.cours,
            "horaire": cours.horairedebut,
            "justifiee": absence.justifiee,
            "motif": absence.motif
        }for cours, absence in zip(cours_passe, absences)]

#Route GET pour récupérer les retards vérifer d'un utilisateur
@router.get("/psw/retard/{id_utilisateur}")
def getURetard(id_utilisateur: int, db: Session = Depends(get_db)):
#Récupération de tous les cours passé
    cours_passe = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == id_utilisateur
    ).all()

    id_cours_passe = [cours.id for cours in cours_passe]
    
#Récupération des retards liées au cours    
    retards = db.query(models.Retard).filter(
        models.Retard.id_edtutilisateur.in_(id_cours_passe),
    ).all()

    if not retards:
        raise HTTPException(status_code = 404, detail = "Retard non trouvé")

    return [{
            "cours": cours.cours,
            "horaire": cours.horairedebut,
            "duree": retard.duree,
            "justifiee": retard.justifiee,
            "motif": retard.motif
        }for cours, retard in zip(cours_passe, retards)]
