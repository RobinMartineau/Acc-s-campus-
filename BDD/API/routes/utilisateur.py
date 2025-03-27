from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
import password

#Instanciation d'un router FastAPI
router = APIRouter()

#Fonction pour récupérer la session de la BDD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Route GET pour récupérer l'entrée correspondant à l'id dans Utilisateur
@router.get("/utilisateur/{id_utilisateur}", response_model = schemas.UtilisateurResponse)
def getUtilisateur(id_utilisateur: int, db: Session = Depends(get_db)):
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == id_utilisateur).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur non trouvée")

    return utilisateur

#Route POST pour ajouter une entrées dans Utilisateur
@router.post("/utilisateur/", response_model = schemas.UtilisateurResponse)
def postUtilisateur(utilisateur: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    
    db_utilisateur = models.Utilisateur(**utilisateur.dict())
    
#Générer l'identifiant unique en minuscule
    identifiant = f"{utilisateur.prenom.lower()}.{utilisateur.nom.lower()}"

#Vérifier si l'identifiant existe déjà
    existant = db.query(models.Utilisateur).filter(models.Utilisateur.identifiant == identifiant).first()
    if existant:
        raise HTTPException(status_code = 400, detail = "Identifiant déjà pris, veuillez modifier le prénom ou le nom")

#Création de l'utilisateur
    db_utilisateur = models.Utilisateur(
        nom = utilisateur.nom,
        prenom = utilisateur.prenom,
        role = utilisateur.role,
        date_de_naissance = utilisateur.date_de_naissance,
        id_classe = utilisateur.id_classe,
        identifiant = identifiant
    )
    
#Vérification qu'une classe est bien associer à l'utilisateur si c'est un élève
    if db_utilisateur.role == "Eleve":
        if not db_utilisateur.id_classe:
            raise HTTPException(status_code = 400, detail = "Classe non indiquée")

        classe = db.query(models.Classe).filter(models.Classe.id == db_utilisateur.id_classe).first()
        if not classe:
            raise HTTPException(status_code = 400, detail = "Classe inexistante")

#Génère un mot de passe aléatoire chiffré non existant dans la base
    while True:
            mot_de_passe = password.generatePassword()
            if not db.query(models.Utilisateur).filter(models.Utilisateur.mot_de_passe == mot_de_passe).first():
                break
                
    db_utilisateur.mot_de_passe = mot_de_passe

#Ajoute l'utilisateur à la base  
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)

    return db_utilisateur