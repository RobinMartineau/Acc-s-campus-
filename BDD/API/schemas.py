from pydantic import BaseModel
from typing import Optional
from enum import Enum
import datetime
import chiffrement

#Création des types ENUM
class RoleEnum(str, Enum):
    Invite = "Invite"
    Personnel = "Personnel"
    Eleve = "Eleve"
    Prof = "Prof"
    Admin = "Admin"

class TypeEquipementEnum(str, Enum):
    BAE = "BAE"
    PEA = "PEA"

#Modèle de Salle
class Salle(BaseModel):
    numero: str
    digicode: Optional[str] = None
    statut: Optional[bool] = None

class SalleCreate(Salle):
    pass

class SalleResponse(Salle):
    id: int

    class Config:
        from_attributes = True

#Modèle de Classe
class Classe(BaseModel):
    nom: str

class ClasseCreate(Classe):
    pass

class ClasseResponse(Classe):
    id: int

    class Config:
        from_attributes = True

#Modèle de Equipement
class Equipement(BaseModel):
    adresse_mac: str
    type: TypeEquipementEnum
    id_salle: int

    class Config:
        arbitrary_types_allowed = True

class EquipementCreate(Equipement):
    pass

class EquipementResponse(Equipement):
    id: int

    class Config:
        from_attributes = True

#Modèle de Utilisateur
class Utilisateur(BaseModel):
    nom: str
    prenom: str
    role: Optional[RoleEnum] = None
    date_de_naissance: Optional[datetime.date] = None
    id_classe: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True

class UtilisateurCreate(Utilisateur):
    mot_de_passe: Optional[str] = None
    
class UtilisateurResponse(Utilisateur):
    id: int
    identifiant: Optional[str] = None
    
    class Config:
        from_attributes = True

#Modèle de Badge
class BadgeBase(BaseModel):
    uid: str
    actif: Optional[bool] = None
    creation: Optional[datetime.date] = None
    id_utilisateur: Optional[int] = None 

class BadgeCreate(BadgeBase):
    pass

class BadgeResponse(BadgeBase):
    class Config:
        from_attributes = True
        

#Modèle de Log
class Log(BaseModel):
    horaire: Optional[datetime.datetime] = None
    id_equipement: int
    uid: str

class LogCreate(Log):
    pass

class LogResponse(Log):
    id: int

    class Config:
        from_attributes = True

#Modèle de EDTSalle
class EDTSalle(BaseModel):
    horairedebut: datetime.datetime
    horairefin: datetime.datetime
    cours: Optional[str] = None
    id_utilisateur: Optional[int] = None
    id_salle: int

class EDTSalleCreate(EDTSalle):
    pass

class EDTSalleResponse(EDTSalle):
    id: int

    class Config:
        from_attributes = True

#Modèle de EDTUtilisateur
class EDTUtilisateur(BaseModel):
    horairedebut: datetime.datetime
    horairefin: datetime.datetime
    cours: Optional[str] = None
    id_salle: int
    id_classe: Optional[int] = None
    id_utilisateur: int

class EDTUtilisateurCreate(EDTUtilisateur):
    pass

class EDTUtilisateurResponse(EDTUtilisateur):
    id: int

    class Config:
        from_attributes = True

#Modèle de Absence
class Absence(BaseModel):
    motif: Optional[str] = None
    justifiee: Optional[bool] = None
    valide: Optional[bool] = None
    id_utilisateur: int
    id_edtutilisateur: int

class AbsenceResponse(Absence):
    id: int

    class Config:
        from_attributes = True

#Modèle de Retard
class Retard(BaseModel):
    duree: int
    motif: Optional[str] = None
    justifiee: Optional[bool] = None
    id_utilisateur: int
    id_edtutilisateur: int

class RetardCreate(Retard):
    pass

class RetardResponse(Retard):
    id: int

    class Config:
        from_attributes = True

#Modèle de EDTClasse
class EDTClasse(BaseModel):
    horairedebut: datetime.datetime
    horairefin: datetime.datetime
    cours: Optional[str] = None
    id_utilisateur: Optional[int] = None
    id_salle: int
    id_classe: int

class EDTClasseCreate(EDTClasse):
    pass

class EDTClasseResponse(EDTClasse):
    id: int

    class Config:
        from_attributes = True

#Modèle de Autorisation
class Autorisation(BaseModel):
    autorisee: Optional[bool] = None
    id_utilisateur: int
    id_salle: int

class AutorisationCreate(Autorisation):
    pass

class AutorisationResponse(Autorisation):
    id: int

    class Config:
        from_attributes = True

#Modèle de Reservation
class Reservation(BaseModel):
    horairedebut: datetime.datetime
    horairefin: datetime.datetime
    id_utilisateur: int
    id_salle: int
    
class ReservationCreate(Reservation):
    pass

class ReservationResponse(Reservation):
    id: int
    id_edtsalle: int
    
    class Config:
        from_attributes = True

#Modèle pour la PEA
class AccesRequest(BaseModel):
    uid: str
    adresse_mac: str

#Modèle pour la BAE
class AppelRequest(BaseModel):
    uid: str
    adresse_mac: str

#Modèle pour le PSW
class LoginRequest(BaseModel):
    identifiant: str
    mot_de_passe: str

#Modèle pour le PGS
class ModifRequest(BaseModel):
    id_utilisateur: int
    nom: Optional[str] = None
    prenom: Optional[str] = None
    role: Optional[RoleEnum] = None
    date_de_naissance: Optional[datetime.date] = None
    id_classe: Optional[int] = None
    
class AssoRequest(BaseModel):
    uid: str
    id_utilisateur: int

class ActiBadge(BaseModel):
    uid: str
    actif: bool

class RecupUtilisateur(Utilisateur):
    id: int
    mot_de_passe: str
    identifiant: Optional[str] = None
    
    #Méthode renvoyer le mot de passe en clair
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id = obj.id,
            nom = obj.nom,
            prenom = obj.prenom,
            role = obj.role,
            date_de_naissance = obj.date_de_naissance,
            mot_de_passe = chiffrement.decryptPassword(obj.mot_de_passe),
            id_classe = obj.id_classe
        )

