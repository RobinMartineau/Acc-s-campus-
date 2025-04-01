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
                        {"id": 1, "nom": "Dupont", "prenom": "Jean", "email": "jean.dupont@example.com", "mot_de_passe": "password123"},
                        {"id": 2, "nom": "Doe", "prenom": "Jane", "email": "jane.doe@example.com", "mot_de_passe": "123456"}
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
)
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
                        "id": 1,
                        "uid": "123ABC456A",
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
)
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

#Associer le badge à l'utilisateur
    badge.id_utilisateur = utilisateur.id

    db.commit()
    db.refresh(badge)

    return badge
