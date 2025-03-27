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

#Modèle de Classe
class Classe(BaseModel):
    nom: str

class ClasseCreate(Classe):
    pass

#Modèle de Equipement
class Equipement(BaseModel):
    adresse_mac: str
    type: TypeEquipementEnum
    id_salle: int

    class Config:
        arbitrary_types_allowed = True

class EquipementCreate(Equipement):
    pass

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

#Modèle de Badge
class BadgeBase(BaseModel):
    uid: str
    actif: Optional[bool] = None
    creation: Optional[datetime.date] = None
    id_utilisateur: Optional[int] = None 

class BadgeCreate(BadgeBase):
    pass

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

#Modèle de Autorisation
class Autorisation(BaseModel):
    autorisee: Optional[bool] = None
    id_utilisateur: int
    id_salle: int

class AutorisationCreate(Autorisation):
    pass

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
    
class AssoRequest(ModifRequest):
    uid: str

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

