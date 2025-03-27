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

#Route POST pour vérifier l'accès d'un utilisateur
@router.post("/pea/acces/")
def verifierAcces(request: schemas.AccesRequest, db: Session = Depends(get_db)):
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

#Convertir l'UID de binaire (40 bits) en octets
    uid_octet = int(uid, 2).to_bytes(5, "big")

#Trouver l’utilisateur lié au badge
    badge = db.query(models.Badge).filter(models.Badge.uid == uid_octet).first()

    if not badge or not badge.id_utilisateur:
        raise HTTPException(status_code = 404, detail = "Badge inconnu ou non associé")

#Vérifier que l'utilisateur existe bel et bien
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == badge.id_utilisateur).first()

    if not utilisateur:
        raise HTTPException(status_code = 404, detail = "Utilisateur inconnu")
  
#Vérifier si le badge est désactivé
    if not badge.actif:
        raise HTTPException(status_code = 403, detail = "Accès refusé : Veuillez rapporter le badge à un membre de la vie scolaire.")

#Trouver la salle correspondant à la PEA
    if not equipement or not equipement.id_salle:
        raise HTTPException(status_code = 404, detail = "Salle non trouvée")

    id_salle = equipement.id_salle

#Vérifier si une autorisation existe pour cet utilisateur dans cette salle
    autorisation = db.query(models.Autorisation).filter(
        models.Autorisation.id_utilisateur == utilisateur.id,
        models.Autorisation.id_salle == id_salle
    ).first()

#Vérifier s'il a un cours en ce moment dans EDTUtilisateur
    cours = db.query(models.EDTUtilisateur).filter(
        models.EDTUtilisateur.id_utilisateur == utilisateur.id,
        models.EDTUtilisateur.id_salle == id_salle,
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
