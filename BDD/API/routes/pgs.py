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

#Route GET pour récupérer tous les utilisateurs avec leur mot de passe en clair
@router.get("/pgs/utilisateur/",
    response_model=list[schemas.RecupUtilisateur],
    summary="Récupérer la liste des utilisateurs",
    description="Cette route permet d'obtenir tous les utilisateurs enregistrés dans la base de données avec leur mot de passe en clair.",
    responses={
        200: {
            "description": "Liste des utilisateurs retournée avec succès",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "nom": "Dupont", "prenom": "Jean", "identifiant": "jean.dupont", "role": "Eleve", "date_de_naissance": "2005-04-01", "mot_de_passe": "Tynego28", "id_classe": "1"},
                        {"id": 1, "nom": "Marie", "prenom": "Frank", "identifiant": "frank.marie", "role": "Prof", "date_de_naissance": "1976-05-11", "mot_de_passe": "Gezaqi71", "id_classe": "null"},
                    ]
                }
            }
        },
        404: {
            "description": "Aucun utilisateur trouvé",
            "content": {
                "application/json": {
                    "example": {"detail": "Aucun utilisateur"}
                }
            }
        },
    }, 
tags=["PGS"])
def getUtilisateurs(db: Session = Depends(get_db)):
    utilisateur = db.query(models.Utilisateur).all()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Aucun utilisateur")

    utilisateur_clair = [schemas.RecupUtilisateur.from_orm(u) for u in utilisateur]
    
    return utilisateur_clair

#Route PUT pour modifier un utilisateur
@router.put("/pgs/modifier/utilisateur/{id_utilisateur}", response_model=schemas.UtilisateurResponse, include_in_schema = False)
def modifierUtilisateur(request: schemas.ModifRequest, utilisateur_update: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    id_utilisateur = request.id_utilisateur

    #Vérifier si l'utilisateur existe
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == id_utilisateur).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur non trouvé")

    #Vérifier si le rôle change pour "Élève"
    if utilisateur_update.role == "Eleve":
        if not utilisateur_update.id_classe:
            raise HTTPException(status_code = 400, detail = "Un élève doit être associé à une classe")

        #Vérifier que la classe existe
        classe = db.query(models.Classe).filter(models.Classe.id == utilisateur_update.id_classe).first()

        if not classe:
            raise HTTPException(status_code = 400, detail = "Classe inexistante")

    #Mettre à jour l'utilisateur
    for key, value in utilisateur_update.dict(exclude_unset = True).items():
        setattr(utilisateur, key, value)

    db.commit()
    db.refresh(utilisateur)

    return utilisateur

#Route PUT pour associer un utilisateur à un badge
@router.put("/pgs/associer/utilisateur/{id_utilisateur}/badge/{uid_badge}",
    summary="Associer un badge à un utilisateur",
    description="Cette route permet d'associer un badge à un utilisateur en fonction de leur ID respectif.",
    responses={
        200: {
            "description": "Badge associé avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "uid": "123ABC45",
                        "id_utilisateur": 2
                    }
                }
            }
        },
        400: {
            "description": "Erreur de validation",
            "content": {
                "application/json": {
                    "examples": {
                        "Badge déjà attribué": {
                            "summary": "Ce badge est déjà utilisé",
                            "value": {"detail": "Ce badge est déjà attribué à un utilisateur"},
                        }
                    }
                }
            },
        },
        404: {
            "description": "Utilisateur ou badge non trouvé",
            "content": {
                "application/json": {
                    "examples": {
                        "Utilisateur introuvable": {
                            "summary": "L'utilisateur spécifié n'existe pas",
                            "value": {"detail": "Utilisateur non trouvé"},
                        },
                        "Badge introuvable": {
                            "summary": "Le badge spécifié n'existe pas",
                            "value": {"detail": "Badge non trouvé"},
                        }
                    }
                }
            },
        },
    }, 
tags=["PGS"])
def associerBadge(request: schemas.AssoRequest, db: Session = Depends(get_db)):
    uid = request.uid
    id_utilisateur = request.id_utilisateur

    #Vérifier si l'utilisateur existe
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == id_utilisateur).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur non trouvé")

    #Vérifier si le badge existe
    badge = db.query(models.Badge).filter(models.Badge.uid == uid).first()

    if not badge:
        raise HTTPException(status_code = 404, detail = "Badge non trouvé")

    #Vérifier si le badge est déjà attribué
    if badge.id_utilisateur:
        raise HTTPException(status_code = 400, detail = "Ce badge est déjà attribué à un utilisateur")

    #Vérifier si l'utilisateur a déjà un badge
    badge_exist = db.query(models.Badge).filter(models.Badge.id_utilisateur == id_utilisateur).first()
    
    if badge_exist:
        raise HTTPException(status_code=400, detail="Cet utilisateur possède déjà un badge")

    #Associer le badge à l'utilisateur
    badge.id_utilisateur = utilisateur.id

    db.commit()
    db.refresh(badge)

    return badge

@router.put("/pgs/dissocier/utilisateur/{id_utilisateur}/badge/{uid_badge}",
    summary="Dissocier un badge d'un utilisateur",
    description="Cette route permet de dissocier un badge actuellement associé à un utilisateur, en utilisant leur ID et l'UID du badge.",
    responses={
        200: {
            "description": "Badge dissocié avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "uid": "123ABC45",
                        "actif": True,
                        "creation": "2025-03-31",
                        "id_utilisateur": None
                    }
                }
            }
        },
        400: {
            "description": "Erreur de validation",
            "content": {
                "application/json": {
                    "examples": {
                        "Badge non attribué": {
                            "summary": "Le badge n'est pas actuellement associé",
                            "value": {"detail": "Ce badge n'est pas déjà attribué à un utilisateur"},
                        }
                    }
                }
            },
        },
        404: {
            "description": "Utilisateur ou badge non trouvé",
            "content": {
                "application/json": {
                    "examples": {
                        "Utilisateur introuvable": {
                            "summary": "L'utilisateur spécifié n'existe pas",
                            "value": {"detail": "Utilisateur non trouvé"},
                        },
                        "Badge introuvable": {
                            "summary": "Le badge spécifié n'existe pas",
                            "value": {"detail": "Badge non trouvé"},
                        }
                    }
                }
            },
        },
    }, 
tags=["PGS"])
def dissocierBadge(request: schemas.AssoRequest, db: Session = Depends(get_db)):
    uid = request.uid
    id_utilisateur = request.id_utilisateur

    #Vérifier si l'utilisateur existe
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == id_utilisateur).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur non trouvé")

    #Vérifier si le badge existe
    badge = db.query(models.Badge).filter(models.Badge.uid == uid).first()

    if not badge:
        raise HTTPException(status_code = 404, detail = "Badge non trouvé")

    #Vérifier si le badge est déjà attribué
    if not badge.id_utilisateur:
        raise HTTPException(status_code = 400, detail = "Ce badge n'est pas déjà attribué à un utilisateur")

    #Dissocier le badge
    badge.id_utilisateur = None

    db.commit()
    db.refresh(badge)

    return badge

#Route PUT pour activer/désactiver un badge
@router.put("/pgs/badge/",
    summary="Activer ou désactiver un badge",
    description=(
        "Cette route permet d'activer ou de désactiver un badge en fonction de son UID. "
        "Si le badge est déjà dans l'état demandé, une erreur 403 est retournée."
    ),
    responses={
        200: {
            "description": "Badge activé ou désactivé avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "uid": "123ABC45",
                        "actif": True
                    }
                }
            }
        },
        403: {
            "description": "Le badge est déjà dans l'état demandé",
            "content": {
                "application/json": {
                    "examples": {
                        "Déjà activé": {
                            "summary": "Le badge est déjà activé",
                            "value": {"detail": "Badge déjà activé."}
                        },
                        "Déjà désactivé": {
                            "summary": "Le badge est déjà désactivé",
                            "value": {"detail": "Badge déjà désactivé."}
                        }
                    }
                }
            }
        },
        404: {
            "description": "Badge non trouvé",
            "content": {
                "application/json": {
                    "example": {"detail": "Badge non trouvé"}
                }
            }
        },
    }, 
tags=["PGS"])
def activerBadge(request: schemas.ActiBadge, db: Session = Depends(get_db)):
    uid = request.uid

    #Vérifier si le badge existe
    badge = db.query(models.Badge).filter(models.Badge.uid == uid).first()

    if not badge:
        raise HTTPException(status_code = 404, detail = "Badge non trouvé")

    #Vérifier si le badge est déjà...
    if badge.actif == request.actif:
        #...Activé
        if request.actif == True:
            raise HTTPException(status_code=403, detail="Badge déjà activé.")
        #...Désactivé
        else:
            raise HTTPException(status_code=403, detail="Badge déjà désactivé.")

    #Associer le badge à l'utilisateur
    badge.actif = request.actif

    db.commit()
    db.refresh(badge)

    return badge
