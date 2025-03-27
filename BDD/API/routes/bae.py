from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import timedelta
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

#Route POST pour faire l'absence d'un cours
@router.post("/bae/appel/")
def faireAbsence(request: schemas.AppelRequest, db: Session = Depends(get_db)):
    uid = request.uid
    adresse_mac = request.adresse_mac

    equipement = db.query(models.Equipement).filter(models.Equipement.adresse_mac == adresse_mac).first()
    heure_actuelle = datetime.datetime.now()

#Vérifier que l'equipement existe
    if not equipement:
        raise HTTPException(status_code = 404, detail = "Équipement introuvable")
 
#Verifier que l'adresse mac correspond bien à une BAE
    if equipement.type == "PEA":
        raise HTTPException(status_code = 400, detail = "Mauvaise requête : contacter un administrateur réseau")
    
#Trouver l’utilisateur lié au badge
    badge = db.query(models.Badge).filter(models.Badge.uid == uid).first()

    if not badge or not badge.id_utilisateur:
        raise HTTPException(status_code = 404, detail = "Badge inconnu ou non associé")

#Vérifier si le badge est désactivé
    if not badge.actif:
        raise HTTPException(status_code = 403, detail = "Accès refusé : Veuillez rapporter le badge à un membre de la vie scolaire.")

#Vérifier que l'utilisateur existe bel et bien
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == badge.id_utilisateur).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur inconnu")

#Trouver la salle correspondant à la PEA
    if not equipement or not equipement.id_salle:
        raise HTTPException(status_code = 404, detail = "Salle non trouvée")

    salle = db.query(models.Salle).filter(models.Salle.id == equipement.id_salle).first()

#Vérifier que l'utilisateur est bien un élève
    if utilisateur.role != "Eleve":
        raise HTTPException(status_code = 403, detail = "Borne d'Absence étudiant, vous n'êtes pas un étudiant")
    
#Vérifier s'il a un cours en ce moment dans EDTUtilisateur   
    cours = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == utilisateur.id,
        models.EDTUtilisateur.id_salle == salle.id,
        models.EDTUtilisateur.horairedebut <= heure_actuelle,
        models.EDTUtilisateur.horairefin >= heure_actuelle
    ).first()

    if not cours:
        cours = db.query(models.EDTUtilisateur).filter(
                models.EDTUtilisateur.id_utilisateur == utilisateur.id,
                models.EDTUtilisateur.horairedebut <= heure_actuelle,
                models.EDTUtilisateur.horairefin >= heure_actuelle
            ).first()
            
        if not cours:
            raise HTTPException(status_code = 403, detail = "Tu n'as pas cours en ce moment")
            
        salle = db.query(models.Salle).filter(models.Salle.id == cours.id_salle).first()      
        raise HTTPException(status_code = 403, detail = f"Tu n'as pas cours dans cette salle, mais en {salle.numero}")
        
            
#Mettre l'utilisateur présent à son cours
    db.query(models.Absence).filter(
        models.Absence.id_utilisateur == utilisateur.id,
        models.Absence.id_edtutilisateur == cours.id
    ).update({"valide": False})
    db.commit()
        
#Ajouter un retard si nécessaire
    limite = cours.horairedebut + timedelta(minutes = 5)
    retard = (heure_actuelle - cours.horairedebut).total_seconds() // 60
    
    if heure_actuelle > limite:  
        retard_entry = models.Retard(
            duree = int(retard),
            id_utilisateur = utilisateur.id,
            id_edtutilisateur = cours.id
        )
        
        db.add(retard_entry)
        db.commit()

#Retourne les données nécessaires
    classe = db.query(models.Classe).filter(models.Classe.id == utilisateur.id_classe).first()
    
    return {
            "nom": utilisateur.nom,
            "prenom": utilisateur.prenom,
            "classe": classe.nom
        }
