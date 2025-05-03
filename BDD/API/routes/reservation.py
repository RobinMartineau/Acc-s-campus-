from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
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

#Route GET pour récupérer toutes les entrées dans Reservation
@router.get("/reservation/", response_model = list[schemas.ReservationResponse], include_in_schema = False)
def getReservations(db: Session = Depends(get_db)):

    return db.query(models.Reservation).all()

#Route GET pour récupérer l'entrée correspondant à  l'id dans Reservation
@router.get("/reservation/{id_reservation}", response_model = schemas.ReservationResponse, include_in_schema = False)
def getReservation(id_reservation: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == id_reservation).first()

    if not reservation:
        raise HTTPException(status_code = 404, detail = "Reservation non trouvée")

    return reservation

#Route POST pour ajouter une entrées dans Reservation
@router.post(
    "/reservation/",
    summary="Ajouter une réservation",
    description=(
        "Cette route permet à un personnel autorisé (hors élèves et invités) d’ajouter une réservation de salle pour une tranche horaire définie.\n\n"
        "Les opérations suivantes sont réalisées :\n"
        "- Vérification de l'existence de l'utilisateur et de son rôle.\n"
        "- Vérification des conflits de réservation pour la salle, l'utilisateur et la classe (si précisée).\n"
        "- Création des entrées dans EDTSalle, EDTUtilisateur, EDTClasse (si applicable), et dans Reservation.\n"
        "- Ajout automatique des cours pour chaque élève de la classe (si présente), sauf en cas de conflit individuel.\n"
    ),
    response_model=schemas.ReservationResponse,
    responses={
        200: {
            "description": "Réservation ajoutée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "id": 42,
                        "horairedebut": "2025-05-01T10:00:00",
                        "horairefin": "2025-05-01T12:00:00",
                        "id_salle": 5,
                        "id_utilisateur": 3,
                        "id_edtsalle": 89
                    }
                }
            }
        },
        403: {
            "description": "Utilisateur non autorisé à réserver",
            "content": {
                "application/json": {
                    "example": {"detail": "Interdit : vous ne pouvez pas réserver une salle"}
                }
            }
        },
        404: {
            "description": "Ressource non trouvée",
            "content": {
                "application/json": {
                    "examples": {
                        "Utilisateur non trouvé": {
                            "summary": "ID utilisateur inexistant",
                            "value": {"detail": "Utilisateur non trouvé"}
                        }
                    }
                }
            }
        },
        409: {
            "description": "Conflit de réservation détecté",
            "content": {
                "application/json": {
                    "examples": {
                        "Salle occupée": {
                            "summary": "Conflit de réservation sur la salle",
                            "value": {"detail": "La salle est déjà réservée sur ce créneau"}
                        },
                        "Utilisateur occupé": {
                            "summary": "Conflit avec une autre réservation de l'utilisateur",
                            "value": {"detail": "L'utilisateur a déjà une réservation sur ce créneau"}
                        },
                        "Classe occupée": {
                            "summary": "Conflit avec une réservation existante de la classe",
                            "value": {"detail": "La classe a déjà une réservation sur ce créneau"}
                        },
                        "Élève occupé": {
                            "summary": "Conflit avec une réservation d’un élève de la classe",
                            "value": {"detail": "L'élève Dupont a déjà une réservation sur ce créneau"}
                        }
                    }
                }
            }
        }
    },
tags=["PGS"])
def postReservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    #Fonction utilitaire pour vérifier les chevauchements de réservation
    def chevauchement_existe(queryset, id_field_name, id_value):
        return db.query(queryset).filter(
            getattr(queryset, id_field_name) == id_value,
            or_(
                and_(
                    reservation.horairedebut >= queryset.horairedebut,
                    reservation.horairedebut < queryset.horairefin,
                ),
                and_(
                    reservation.horairefin > queryset.horairedebut,
                    reservation.horairefin <= queryset.horairefin,
                ),
                and_(
                    reservation.horairedebut <= queryset.horairedebut,
                    reservation.horairefin >= queryset.horairefin,
                ),
            )
        ).first() is not None

    #Vérifier si l'utilisateur existe
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == reservation.id_utilisateur).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    #Vérification du rôle
    if utilisateur.role in ["Eleve", "Invite"]:
        raise HTTPException(status_code=403, detail="Interdit : vous ne pouvez pas réserver une salle")

    #Vérifier que la salle existe
    salle = db.query(models.Salle).filter(models.Salle.id == reservation.id_salle).first()
    if not salle:
        raise HTTPException(status_code=404, detail="Salle non trouvée")

    #Vérifier que la date de fin est après la date de début
    if reservation.horairefin <= reservation.horairedebut:
        raise HTTPException(status_code=400, detail="Horaire de fin doit être après l'horaire de début")

    #Vérification du chevauchement pour la salle
    if chevauchement_existe(models.EDTSalle, "id_salle", reservation.id_salle):
        raise HTTPException(status_code=403, detail="La salle est déjà réservée sur ce créneau")

    #Création dans EDTSalle
    creneau_salle = models.EDTSalle(
        horairedebut=reservation.horairedebut,
        horairefin=reservation.horairefin,
        id_utilisateur=reservation.id_utilisateur,
        id_salle=reservation.id_salle,
        id_classe=reservation.id_classe
    )
    db.add(creneau_salle)
    db.commit()
    db.refresh(creneau_salle)

    #Vérif chevauchement pour l'utilisateur
    if chevauchement_existe(models.EDTUtilisateur, "id_utilisateur", reservation.id_utilisateur):
        raise HTTPException(status_code=403, detail="L'utilisateur a déjà une réservation sur ce créneau")

    #Création dans EDTUtilisateur
    creneau_utilisateur = models.EDTUtilisateur(
        horairedebut=reservation.horairedebut,
        horairefin=reservation.horairefin,
        id_utilisateur=reservation.id_utilisateur,
        id_salle=reservation.id_salle,
        id_classe=reservation.id_classe
    )
    db.add(creneau_utilisateur)
    db.commit()
    db.refresh(creneau_utilisateur)

    eleves = []
    if reservation.id_classe is not None:
        #Vérifier que la classe existe
        classe = db.query(models.Classe).filter(models.Classe.id == reservation.id_classe).first()
        if not classe:
            raise HTTPException(status_code=404, detail="Classe non trouvée")

        #Vérification du chevauchement pour la classe
        if chevauchement_existe(models.EDTClasse, "id_classe", reservation.id_classe):
            raise HTTPException(status_code=403, detail="La classe a déjà une réservation sur ce créneau")

        #Création dans EDTClasse
        creneau_classe = models.EDTClasse(
            horairedebut=reservation.horairedebut,
            horairefin=reservation.horairefin,
            id_utilisateur=reservation.id_utilisateur,
            id_salle=reservation.id_salle,
            id_classe=reservation.id_classe
        )
        db.add(creneau_classe)
        db.commit()
        db.refresh(creneau_classe)

        #Récupération des élèves
        eleves = db.query(models.Utilisateur).filter(models.Utilisateur.id_classe == reservation.id_classe).all()

        #Vérification du chevauchement pour chaque élève
        for eleve in eleves:
            if chevauchement_existe(models.EDTUtilisateur, "id_utilisateur", eleve.id):
                raise HTTPException(status_code=403, detail=f"L'élève {eleve.nom} a déjà une réservation sur ce créneau")

        #Création des entrées EDTUtilisateur pour les élèves
        for eleve in eleves:
            cours_utilisateur = models.EDTUtilisateur(
                horairedebut=reservation.horairedebut,
                horairefin=reservation.horairefin,
                id_utilisateur=eleve.id,
                id_salle=reservation.id_salle,
                id_classe=reservation.id_classe
            )
            db.add(cours_utilisateur)
            db.commit()
            db.refresh(cours_utilisateur)

    #Création finale dans Reservation
    new_reservation = models.Reservation(
        horairedebut=reservation.horairedebut,
        horairefin=reservation.horairefin,
        id_salle=reservation.id_salle,
        id_utilisateur=reservation.id_utilisateur,
        id_edtsalle=creneau_salle.id
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation


#Route DELETE pour supprimer l'entrée correspondant à l'id dans Reservation
@router.delete("/reservation/{id_reservation}", include_in_schema = False)
def deleteReservation(id_reservation: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == id_reservation).first()

    if not reservation:
        raise HTTPException(status_code = 404, detail = "Reservation non trouvée")

    db.delete(reservation)
    db.commit()

    return
