from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
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

#Route POST pour la connexion
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
                    "example": {"detail": "Mot de passe incorrect"}
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
        raise HTTPException(status_code = 401, detail = "Mot de passe incorrect")
        
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

    if not classe:
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

#Route GET pour récupérer l'activité dans une salle en temps réel (emploie du temps et utilisateurs présent)
@router.get(
    "/psw/salle/{id_salle}/activite",
    summary="Obtenir les activités d'une salle",
    description=(
        "Cette route permet d'obtenir :\n\n"
        "- Les réservations (EDTSalle) liées à une salle (horaire, cours, utilisateur associé).\n"
        "- La liste des utilisateurs ayant utilisé leur badge dans cette salle il y a moins d'une heure (dernier badge uniquement).\n"
        "- Le nombre total de ces utilisateurs ayant badgé.\n"
    ),
    responses={
        200: {
            "description": "Réservations et utilisateurs récupérés avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "reservations": [
                            {
                                "horairedebut": "2025-04-10T08:00:00",
                                "horairefin": "2025-04-10T09:00:00",
                                "cours": "Maths",
                                "utilisateur": {
                                    "id": 12,
                                    "nom": "Lemoine",
                                    "prenom": "Arthur"
                                }
                            }
                        ],
                        "utilisateurs_derniere_heure": [
                            {
                                "id": 12,
                                "nom": "Lemoine",
                                "prenom": "Arthur"
                            },
                            {
                                "id": 17,
                                "nom": "Benoit",
                                "prenom": "Lucie"
                            }
                        ],
                        "nombre_utilisateurs": 2
                    }
                }
            }
        },
        404: {
            "description": "Ressources manquantes ou erreur de cohérence",
            "content": {
                "application/json": {
                    "examples": {
                        "Salle introuvable": {
                            "summary": "ID de salle invalide",
                            "value": {"detail": "Salle non trouvée"}
                        },
                        "Aucune réservation": {
                            "summary": "Aucun cours enregistré dans cette salle",
                            "value": {"detail": "Aucune réservation trouvée pour cette salle"}
                        },
                        "Réservation sans utilisateur": {
                            "summary": "Erreur de données",
                            "value": {"detail": "Réservation sans utilisateur associée (ID réservation 23)"}
                        },
                        "Utilisateur réservation inconnu": {
                            "summary": "Utilisateur non présent en base",
                            "value": {"detail": "Utilisateur (ID 8) introuvable pour une réservation"}
                        },
                        "Badge introuvable": {
                            "summary": "Badge UID non présent",
                            "value": {"detail": "Badge UID A1B2 introuvable"}
                        },
                        "Badge non associé": {
                            "summary": "Badge sans utilisateur",
                            "value": {"detail": "Badge UID A1B2 non associé à un utilisateur"}
                        },
                        "Utilisateur badge introuvable": {
                            "summary": "Utilisateur non trouvé pour badge",
                            "value": {"detail": "Utilisateur ID 9 introuvable pour badge UID A1B2"}
                        },
                        "Aucun utilisateur final": {
                            "summary": "Aucune ligne valide trouvée",
                            "value": {"detail": "Aucun utilisateur valide ayant badgé dans l'heure"}
                        }
                    }
                }
            }
        }
    },
tags=["PSW"])
def activiteSalle(id_salle: int, db: Session = Depends(get_db)):
    #Vérification de l'existence de la salle
    salle = db.query(models.Salle).filter(
        models.Salle.id == id_salle
        ).first()
    if not salle:
        raise HTTPException(status_code=404, detail="Salle non trouvée")

    #Récupérer les réservations
    edtsalle = db.query(models.EDTSalle).filter(
        models.EDTSalle.id_salle == id_salle
        ).all()
    if not edtsalle:
        raise HTTPException(status_code=404, detail="Aucune réservation trouvée pour cette salle")

    reservations = []
    for res in edtsalle:
        if not res.id_utilisateur:
            raise HTTPException(status_code=404, detail=f"Réservation sans utilisateur associée")

        utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == res.id_utilisateur).first()
        if not utilisateur:
            raise HTTPException(status_code=404, detail=f"Utilisateur introuvable pour une réservation")

        reservations.append({
            "horairedebut": res.horairedebut,
            "horairefin": res.horairefin,
            "cours": res.cours,
            "utilisateur": {
                "id": utilisateur.id,
                "nom": utilisateur.nom,
                "prenom": utilisateur.prenom
            }
        })

    #Logs de badge dans l'heure passée
    il_y_a_une_heure = datetime.datetime.now() - datetime.timedelta(hours=1)

    subquery = (
        db.query(
            models.Log.uid,
            func.max(models.Log.horaire).label("dernier_passage")
        )
        .group_by(models.Log.uid)
        .subquery()
    )

    logs_recents = (
        db.query(models.Log)
        .join(models.Equipement, models.Log.id_equipement == models.Equipement.id)
        .join(subquery, models.Log.uid == subquery.c.uid)
        .filter(
            models.Equipement.id_salle == id_salle,
            models.Log.horaire == subquery.c.dernier_passage,
            models.Log.horaire >= il_y_a_une_heure
        )
        .all()
    )

    utilisateurs_derniere_heure = []
    
    for log in logs_recents:
        badge = db.query(models.Badge).filter(models.Badge.uid == log.uid).first()
        if badge is None:
            raise HTTPException(status_code=404, detail="Badge non trouvé.")
        
        if badge.id_utilisateur is None:
            raise HTTPException(status_code=404, detail="Badge non associé à un utilisateur.")
        
        utilisateur_badge = db.query(models.Utilisateur).filter(models.Utilisateur.id == badge.id_utilisateur).first()
        if utilisateur_badge is None:
            raise HTTPException(status_code=404, detail="Utilisateur du badge non trouvé.")

        utilisateurs_derniere_heure.append(utilisateur_badge)

    return {
        "reservations": reservations,
        "utilisateurs_derniere_heure": utilisateurs_derniere_heure,
        "nombre_utilisateurs": len(utilisateurs_derniere_heure)
    }


