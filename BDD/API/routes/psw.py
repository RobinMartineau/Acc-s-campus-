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
    summary="Se connecter au site web.",
    description="Cette route permet de se connecter au site web.",
    responses={
        200: {
            "description": "Connexion réussie",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "id_utilisateur": 1,
                        "role": "Admin"
                    }
                }
            }
        },
        404: {
            "description": "Utilisateur introuvable",
            "content": {
                "application/json": {
                    "example": {"detail": "Utilisateur introuvable"}
                }
            }
        },
        401: {
            "description": "Mot de passe incorrect",
            "content": {
                "application/json": {
                    "example": {"success": False}
                }
            }
        }
    }, 
tags=["PSW"])
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
    summary="Récupérer la liste des absences",
    description="Cette route permet d'obtenir toutes les absences d'un utilisateur",
    responses={
        200: {
            "description": "Absences récupérées avec succès",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "cours": "Mathématiques",
                            "horaire": "2025-03-31T08:00:00",
                            "justifiee": True,
                            "motif": "Maladie"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Absences non trouvées",
            "content": {
                "application/json": {
                    "example": {"detail": "Absences non trouvées"}
                }
            }
        }
    }, 
tags=["PSW"])
def getUAbsence(id_utilisateur: int, db: Session = Depends(get_db)):  
    heure_actuelle = datetime.datetime.now()
    
    #Récupération de tous les cours passé
    cours_passe = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == id_utilisateur,
        models.EDTUtilisateur.horairefin <= heure_actuelle
    ).all()

    id_cours = [cours.id for cours in cours_passe]
    
    #Récupération des absences liées au cours
    absences = db.query(models.Absence).filter(
        models.Absence.id_edtutilisateur.in_(id_cours),
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

#Route GET pour récupérer les retards d'un utilisateur
@router.get("/psw/retard/{id_utilisateur}",
    summary="Récupérer la liste des retards",
    description="Cette route permet d'obtenir tous les retards d'un utilisateur",
    responses={
        200: {
            "description": "Retards récupérés avec succès",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "cours": "Physique",
                            "horaire": "2025-03-31T09:00:00",
                            "duree": 15,
                            "justifiee": False,
                            "motif": "Transport en retard"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Retards non trouvés",
            "content": {
                "application/json": {
                    "example": {"detail": "Retards non trouvés"}
                }
            }
        }
    }, 
tags=["PSW"])
def getURetard(id_utilisateur: int, db: Session = Depends(get_db)):
    heure_actuelle = datetime.datetime.now()

    #Récupération de tous les cours passé
    cours_passe = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == id_utilisateur,
        models.EDTUtilisateur.horairefin <= heure_actuelle
    ).all()

    id_cours = [cours.id for cours in cours_passe]
    
    #Récupération des retards liées au cours    
    retards = db.query(models.Retard).filter(
        models.Retard.id_edtutilisateur.in_(id_cours),
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
    summary="Récupérer la liste des élèves",
    description="Cette route permet d'obtenir les noms, prénoms et classes de tous les élèves",
    responses={
        200: {
            "description": "Élèves récupérés avec succès",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "nom": "Dupont",
                            "prenom": "Jean",
                            "classe": "CIEL"
                        }
                    ]
                }
            }
        },
        404: {
            "description": "Élèves non trouvés",
            "content": {
                "application/json": {
                    "examples": {
                        "Aucuns élèves": {
                            "summary": "Élèves non trouvés",
                            "value": {"detail": "Élèves non trouvés"},
                        },
                        "Aucunes classes": {
                            "summary": "Classes non trouvées",
                            "value": {"detail": "Classes non trouvées"},
                        }
                    }
                }
            }
        }
    }, 
tags=["PSW"])
def getEleve(db: Session = Depends(get_db)):
    eleve = db.query(models.Utilisateur).filter(
        models.Utilisateur.role == "Eleve"
    ).all()

    if not eleve:
        raise HTTPException(status_code = 404, detail = "Élèves non trouvés")        

    id_classe = [utilisateur.id_classe for utilisateur in eleve]
    
    classe = db.query(models.Classe).filter(
            models.Classe.id.in_(id_classe)
        ).all()

    if not eleve:
        raise HTTPException(status_code = 404, detail = "Classes non trouvées")
 
    classes_dict = {c.id: c.nom for c in classe}

    return [
        {
            "id": utilisateur.id,
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "classe": classes_dict.get(utilisateur.id_classe, "Inconnue")
        }
        for utilisateur in eleve
    ]
