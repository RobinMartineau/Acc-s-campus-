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
@router.post("/psw/login/",
    responses={
        200: {"description": "Connexion réussie"},
        404: {"description": "Utilisateur introuvable"},
        401: {"description": "Mot de passe incorrect"},
    },
)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.identifiant == request.identifiant).first()

    #Vérifier si l'utilisateur existe
    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur introuvable")

    #Vérifier le mot de passe
    mot_de_passe = chiffrement.decryptPassword(utilisateur.mot_de_passe)

    if mot_de_passe != request.mot_de_passe:
        raise {"success": False}
        
    return {
            "success": True,
            "id_utilisateur": utilisateur.id,
            "role": utilisateur.role     
        }

#Route GET pour récupérer les absences vérifer d'un utilisateur
@router.get("/psw/absence/{id_utilisateur}",
    responses={
        200: {"description": "Absences récupérées avec succès"},
        404: {"description": "Absences non trouvées"},
    },
)
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
        raise HTTPException(status_code = 404, detail = "Absences non trouvées")

    return [{
            "cours": cours.cours,
            "horaire": cours.horairedebut,
            "justifiee": absence.justifiee,
            "motif": absence.motif
        }for cours, absence in zip(cours_passe, absences)]

#Route GET pour récupérer les retards vérifer d'un utilisateur
@router.get("/psw/retard/{id_utilisateur}",
    responses={
        200: {"description": "Retards récupérés avec succès"},
        404: {"description": "Retards non trouvés"},
    },
)
def getURetard(id_utilisateur: int, db: Session = Depends(get_db)):
    heure_actuelle = datetime.datetime.now()

    #Récupération de tous les cours passé
    cours_passe = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == id_utilisateur,
        models.EDTUtilisateur.horairefin <= heure_actuelle
    ).all()

    id_cours_passe = [cours.id for cours in cours_passe]
    
    #Récupération des retards liées au cours    
    retards = db.query(models.Retard).filter(
        models.Retard.id_edtutilisateur.in_(id_cours_passe),
    ).all()

    if not retards:
        raise HTTPException(status_code = 404, detail = "Retards non trouvés")

    return [{
            "cours": cours.cours,
            "horaire": cours.horairedebut,
            "duree": retard.duree,
            "justifiee": retard.justifiee,
            "motif": retard.motif
        }for cours, retard in zip(cours_passe, retards)]

#Route GET pour récupérer tout les élèves
@router.get("/psw/eleve",
    responses={
        200: {"description": "Elèves récupérés avec succès"},
        404: {"description": "Elèves non trouvés"},
    },
)
def getEleve(id_utilisateur: int, db: Session = Depends(get_db)):
    eleve = db.query(models.Utilisateur).filter(
        models.Utilisateur.role == "Eleve"
    ).all()

    if not eleve:
        raise HTTPException(status_code = 404, detail = "Elèves non trouvés")        

    return eleve
