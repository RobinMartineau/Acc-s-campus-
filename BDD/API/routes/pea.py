from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
import models
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

#Route POST pour vérifier l'accès d'un utilisateur via badge
@router.post("/pea/acces/badge",
    summary="Vérifier accès via Badge.",
    description="Cette route permet d'autoriser ou non un utilisateur à rentrer dans une salle via badge.",
    responses={
        200: {
            "description": "Accès autorisé",
            "content": {
                "application/json": {
                    "example": {
                        "nom": "Dupont",
                        "prenom": "Jean",
                        "role": "Eleve",
                        "autorisee": True
                    }
                }
            }
        },
        400: {
            "description": "Requête incorrecte (ex: Mauvais type d'équipement)",
            "content": {
                "application/json": {
                    "example": {"detail": "Mauvaise requête: contacter un administrateur réseau"}
                }
            }
        },
        403: {
            "description": "Accès refusé (Badge désactivé ou utilisateur non autorisé)",
            "content": {
                "application/json": {
                    "examples": {
                        "Badge désactivé": {
                            "summary": "Le badge n'est pas actif",
                            "value": {"detail": "Accès refusé : Veuillez rapporter le badge à un membre de la vie scolaire."}
                        },
                        "Autorisation refusée": {
                            "summary": "L'utilisateur n'est pas autorisé à entrer",
                            "value": {"detail": "Accès refusé"}
                        }
                    }
                }
            }
        },
        404: {
            "description": "Ressource introuvable (Équipement, Badge, Utilisateur ou Salle)",
            "content": {
                "application/json": {
                    "examples": {
                        "Équipement introuvable": {
                            "summary": "Adresse MAC inconnue",
                            "value": {"detail": "Équipement introuvable"}
                        },
                        "Badge inconnu": {
                            "summary": "UID du badge non enregistré",
                            "value": {"detail": "Badge inconnu ou non associé"}
                        },
                        "Utilisateur introuvable": {
                            "summary": "L'utilisateur associé au badge n'existe pas",
                            "value": {"detail": "Utilisateur inconnu"}
                        },
                        "Salle introuvable": {
                            "summary": "La salle liée à l'équipement n'existe pas",
                            "value": {"detail": "Salle non trouvée"}
                        }
                    }
                }
            }
        }
    }, 
tags=["PEA"])
def verifierAccesBadge(request: schemas.AccesRequestB, db: Session = Depends(get_db)):
    uid = request.uid
    adresse_mac = request.adresse_mac

    equipement = db.query(models.Equipement).filter(models.Equipement.adresse_mac == adresse_mac).first()
    heure_actuelle = datetime.datetime.now()

    #Vérifier que l'equipement existe
    if not equipement:
        raise HTTPException(status_code = 404, detail = "Équipement introuvable")

    #Vérifier que l'adresse mac correspond bien à une PEA
    if equipement.type == "BAE": 
        raise HTTPException(status_code = 400, detail = "Mauvaise requête: contacter un administrateur réseau")

    #Trouver l’utilisateur lié au badge
    badge = db.query(models.Badge).filter(models.Badge.uid == uid).first()

    if not badge or not badge.id_utilisateur:
        raise HTTPException(status_code = 404, detail = "Badge inconnu ou non associé")

    #Vérifier que l'utilisateur existe bel et bien
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == badge.id_utilisateur).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur inconnu")

    #Ajouter une entrée dans Log
    log_entry = models.Log(
        horaire=heure_actuelle,
        id_equipement=equipement.id,
        uid=uid
    )
    
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
  
    #Vérifier si le badge est désactivé
    if not badge.actif:
        raise HTTPException(status_code = 403, detail = "Accès refusé : Veuillez rapporter le badge à un membre de la vie scolaire.")
        
    #Trouver la salle correspondant à la PEA
    salle = db.query(models.Salle).filter(models.Salle.id == equipement.id_salle).first()

    if not salle:
        raise HTTPException(status_code = 404, detail = "Salle non trouvée")

    #Vérifier si une autorisation existe pour cet utilisateur dans cette salle
    autorisation = db.query(models.Autorisation).filter(
        models.Autorisation.id_utilisateur == utilisateur.id,
        models.Autorisation.id_salle == salle.id
    ).first()

    #Vérifier s'il a un cours en ce moment dans EDTUtilisateur
    cours = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == utilisateur.id,
        models.EDTUtilisateur.id_salle == salle.id,
        models.EDTUtilisateur.horairedebut <= heure_actuelle,
        models.EDTUtilisateur.horairefin >= heure_actuelle
    ).first()

    #Déterminer si l'utilisateur est autorisé
    if autorisation:
        est_autorise = autorisation.autorisee
    else:
        est_autorise = bool(cours)
            
    #Refus de l'accès si l'utilisateur n'est pas autorisé
    if not est_autorise:
        raise HTTPException(status_code = 403, detail = "Accès refusé")

    return {
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom,
        "role": utilisateur.role,
        "autorisee": est_autorise
    }

#Route POST pour vérifier l'accès d'un utilisateur via digicode
@router.post("/pea/acces/digicode",
    summary="Vérifier accès via digicode.",
    description="Cette route permet de vérifier si un utilisateur, identifié par un digicode, est autorisé à entrer dans une salle contrôlée par une PEA. "
                "L'utilisateur doit avoir un badge actif associé, et soit être autorisé explicitement via une autorisation, soit avoir un cours en cours dans la salle.",
    responses={
        200: {
            "description": "Accès autorisé",
            "content": {
                "application/json": {
                    "example": {
                        "nom": "Dupont",
                        "prenom": "Jean",
                        "role": "Eleve",
                        "autorisee": True
                    }
                }
            }
        },
        400: {
            "description": "Requête incorrecte (ex: Mauvais type d'équipement)",
            "content": {
                "application/json": {
                    "example": {"detail": "Mauvaise requête: contacter un administrateur réseau"}
                }
            }
        },
        403: {
            "description": "Accès refusé (badge désactivé ou accès non autorisé)",
            "content": {
                "application/json": {
                    "examples": {
                        "Badge désactivé": {
                            "summary": "Le badge associé est désactivé",
                            "value": {"detail": "Accès refusé : Badge désactivé."}
                        },
                        "Autorisation refusée": {
                            "summary": "L'utilisateur n'est pas autorisé à entrer",
                            "value": {"detail": "Accès refusé"}
                        }
                    }
                }
            }
        },
        404: {
            "description": "Ressource introuvable (Équipement, utilisateur, badge ou salle)",
            "content": {
                "application/json": {
                    "examples": {
                        "Équipement introuvable": {
                            "summary": "Adresse MAC inconnue",
                            "value": {"detail": "Équipement introuvable"}
                        },
                        "Utilisateur inconnu": {
                            "summary": "Le digicode ne correspond à aucun utilisateur",
                            "value": {"detail": "Utilisateur inconnu"}
                        },
                        "Badge non associé": {
                            "summary": "L'utilisateur n'a pas de badge associé",
                            "value": {"detail": "Aucun badge associé"}
                        },
                        "Salle introuvable": {
                            "summary": "La salle liée à l'équipement n'existe pas",
                            "value": {"detail": "Salle non trouvée"}
                        }
                    }
                }
            }
        }
    },
tags=["PEA"])
def verifierAccesDigicode(request: schemas.AccesRequestD, db: Session = Depends(get_db)):
    digicode = request.digicode
    adresse_mac = request.adresse_mac

    equipement = db.query(models.Equipement).filter(models.Equipement.adresse_mac == adresse_mac).first()
    heure_actuelle = datetime.datetime.now()

    #Vérifier que l'equipement existe
    if not equipement:
        raise HTTPException(status_code = 404, detail = "Équipement introuvable")

    #Vérifier que l'adresse mac correspond bien à une PEA
    if equipement.type == "BAE": 
        raise HTTPException(status_code = 400, detail = "Mauvaise requête: contacter un administrateur réseau")

    #Trouver l’utilisateur lié au digicode
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.digicode == digicode).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur inconnu")

    #Trouver le badge lié à l'utilisateur
    badge = db.query(models.Badge).filter(models.Badge.id_utilisateur == utilisateur.id).first()

    if not badge or not badge.id_utilisateur:
        raise HTTPException(status_code = 404, detail = "Aucun badge associé")

    #Ajouter une entrée dans Log
    log_entry = models.Log(
        horaire = heure_actuelle,
        id_equipement = equipement.id,
        uid = badge.uid
    )
    
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
  
    #Vérifier si le badge est désactivé
    if not badge.actif:
        raise HTTPException(status_code = 403, detail = "Accès refusé : Badge désactivé.")

    #Trouver la salle correspondant à la PEA
    salle = db.query(models.Salle).filter(models.Salle.id == equipement.id_salle).first()

    if not salle:
        raise HTTPException(status_code = 404, detail = "Salle non trouvée")

    #Vérifier si une autorisation existe pour cet utilisateur dans cette salle
    autorisation = db.query(models.Autorisation).filter(
        models.Autorisation.id_utilisateur == utilisateur.id,
        models.Autorisation.id_salle == salle.id
    ).first()

    #Vérifier s'il a un cours en ce moment dans EDTUtilisateur
    cours = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == utilisateur.id,
        models.EDTUtilisateur.id_salle == salle.id,
        models.EDTUtilisateur.horairedebut <= heure_actuelle,
        models.EDTUtilisateur.horairefin >= heure_actuelle
    ).first()

    #Déterminer si l'utilisateur est autorisé
    if autorisation:
        est_autorise = autorisation.autorisee
    else:
        est_autorise = bool(cours)
            
    #Refus de l'accès si l'utilisateur n'est pas autorisé
    if not est_autorise:
        raise HTTPException(status_code = 403, detail = "Accès refusé")

    return {
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom,
        "role": utilisateur.role,
        "autorisee": est_autorise
    }
