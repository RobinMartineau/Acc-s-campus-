from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Salle(Base):
    __tablename__ = "salle"

    id = Column(SmallInteger, primary_key = True, autoincrement = True, index = True)
    numero = Column(String(4), unique = True, nullable = False)
    digicode = Column(String(4), nullable = True)
    statut = Column(Boolean, nullable = False, default = False)
    
class Classe(Base):
    __tablename__ = "classe"

    id = Column(SmallInteger, primary_key = True, autoincrement = True, index = True)
    nom = Column(String(20), unique = True, nullable = False)

class Equipement(Base):
    __tablename__ = "equipement"

    id = Column(SmallInteger, primary_key = True, autoincrement = True)
    adresse_mac = Column(String(17), unique = True, nullable = False) 
    type = Column(Enum('BAE', 'PEA', name = "type_enum"), nullable = False)
    id_salle = Column(SmallInteger, ForeignKey("salle.id"), nullable = True)

    salle = relationship("Salle")

class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id = Column(Integer, primary_key = True, autoincrement = True, index = True)
    identifiant = Column(String(61), nullable = False, unique = True)
    mot_de_passe = Column(String(150), nullable = True, unique = True)
    nom = Column(String(30), nullable = True)
    prenom = Column(String(30), nullable = False)
    role = Column(Enum('Invite', 'Personnel', 'Eleve', 'Prof', 'Admin', name = "role_enum"), nullable = False)
    date_de_naissance = Column(Date, nullable = True)
    id_classe = Column(SmallInteger, ForeignKey("classe.id"), nullable = True)

    classe = relationship("Classe")

class Badge(Base):
    __tablename__ = "badge"

    uid = Column(String(10), primary_key = True, index = True)
    actif = Column(Boolean, nullable = False, default = False)
    creation = Column(Date, nullable = False, default = datetime.date.today)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id"), unique = True, nullable = True)

    utilisateur = relationship("Utilisateur")
    
class EDTUtilisateur(Base):
    __tablename__ = "edtutilisateur"

    id = Column(Integer, primary_key = True, autoincrement = True)
    horairedebut = Column(DateTime, nullable = False)
    horairefin = Column(DateTime, nullable = False)
    cours = Column(String(20), nullable = True)
    id_classe = Column(Integer, ForeignKey("classe.id"), nullable = True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id"), nullable = True)
    id_salle = Column(SmallInteger, ForeignKey("salle.id"), nullable = False)

    classe = relationship("Classe")
    utilisateur = relationship("Utilisateur")
    salle = relationship("Salle")
    
class Absence(Base):
    __tablename__ = "absence"

    id = Column(Integer, primary_key = True, autoincrement = True)
    motif = Column(String(50), nullable = True)
    justifiee = Column(Boolean, nullable = False, default = False)
    valide = Column(Boolean, nullable = False, default = True)
    id_utilisateur = Column(Integer,  ForeignKey("utilisateur.id"), nullable = False)
    id_edtutilisateur = Column(Integer,  ForeignKey("edtutilisateur.id"), nullable = False)

    utilisateur = relationship("Utilisateur")
    edtutilisateur = relationship("EDTUtilisateur")

class Retard(Base):
    __tablename__ = "retard"

    id = Column(Integer, primary_key = True, autoincrement = True)
    duree = Column(Integer, nullable = False)
    motif = Column(String(50), nullable = True)
    justifiee = Column(Boolean, nullable = False, default = False)
    id_utilisateur = Column(Integer,  ForeignKey("utilisateur.id"), nullable = False)
    id_edtutilisateur = Column(Integer,  ForeignKey("edtutilisateur.id"), nullable = False)

    utilisateur = relationship("Utilisateur")
    edtutilisateur = relationship("EDTUtilisateur")    

class Autorisation(Base):
    __tablename__ = "autorisation"

    id = Column(Integer, primary_key = True, autoincrement = True) 
    autorisee = Column(Boolean, nullable = False, default = False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id"), nullable = False)
    id_salle = Column(SmallInteger, ForeignKey("salle.id"), nullable = False)

    utilisateur = relationship("Utilisateur")
    salle = relationship("Salle")
