from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Salle(Base):
    __tablename__ = "salle"

    id = Column(SmallInteger, primary_key=True, autoincrement=True, index=True)
    numero = Column(String(4), unique=True, nullable=False)
    statut = Column(Boolean, nullable=False, default=False)

    equipements = relationship("Equipement", back_populates="salle", cascade="all, delete")
    reservations = relationship("Reservation", back_populates="salle", cascade="all, delete")
    edtsalle = relationship("EDTSalle", back_populates="salle", cascade="all, delete")
    edtutilisateur = relationship("EDTUtilisateur", back_populates="salle", cascade="all, delete")
    edtclasse = relationship("EDTClasse", back_populates="salle", cascade="all, delete")
    autorisations = relationship("Autorisation", back_populates="salle", cascade="all, delete")

class Classe(Base):
    __tablename__ = "classe"

    id = Column(SmallInteger, primary_key=True, autoincrement=True, index=True)
    nom = Column(String(20), unique=True, nullable=False)

    utilisateurs = relationship("Utilisateur", back_populates="classe", cascade="all, delete")
    edtsalle = relationship("EDTSalle", back_populates="classe", cascade="all, delete")
    edtutilisateur = relationship("EDTUtilisateur", back_populates="classe", cascade="all, delete")
    edtclasse = relationship("EDTClasse", back_populates="classe", cascade="all, delete")
    reservations = relationship("Reservation", back_populates="classe", cascade="all, delete")

class Equipement(Base):
    __tablename__ = "equipement"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    adresse_mac = Column(String(17), unique=True, nullable=False)
    type = Column(Enum('BAE', 'PEA', name="type_enum"), nullable=False)
    id_salle = Column(SmallInteger, ForeignKey("salle.id", ondelete="CASCADE"), nullable=True)

    salle = relationship("Salle", back_populates="equipements")
    logs = relationship("Log", back_populates="equipement", cascade="all, delete-orphan")

class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    identifiant = Column(String(61), nullable=False, unique=True)
    mot_de_passe = Column(String(150), nullable=True, unique=True)
    nom = Column(String(30), nullable=True)
    prenom = Column(String(30), nullable=False)
    role = Column(Enum('Invite', 'Personnel', 'Eleve', 'Prof', 'Admin', name="role_enum"), nullable=False)
    digicode = Column(String(4), nullable=True)
    date_de_naissance = Column(Date, nullable=True)
    id_classe = Column(SmallInteger, ForeignKey("classe.id", ondelete="CASCADE"), nullable=True)

    classe = relationship("Classe", back_populates="utilisateurs")
    badge = relationship("Badge", back_populates="utilisateur", cascade="all, delete", uselist=False)
    absences = relationship("Absence", back_populates="utilisateur", cascade="all, delete")
    retards = relationship("Retard", back_populates="utilisateur", cascade="all, delete")
    reservations = relationship("Reservation", back_populates="utilisateur", cascade="all, delete")
    autorisations = relationship("Autorisation", back_populates="utilisateur", cascade="all, delete")
    edtutilisateur = relationship("EDTUtilisateur", back_populates="utilisateur", cascade="all, delete")
    edtclasse = relationship("EDTClasse", back_populates="utilisateur", cascade="all, delete")
    edtsalle = relationship("EDTSalle", back_populates="utilisateur", cascade="all, delete")

class Badge(Base):
    __tablename__ = "badge"

    uid = Column(String(8), primary_key=True, index=True)
    actif = Column(Boolean, nullable=False, default=False)
    creation = Column(Date, nullable=False, default=datetime.date.today)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), unique=True, nullable=True)

    utilisateur = relationship("Utilisateur", back_populates="badge")
    logs = relationship("Log", back_populates="badge", cascade="all, delete-orphan")

class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    horaire = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    id_equipement = Column(SmallInteger, ForeignKey("equipement.id", ondelete="CASCADE"), nullable=False)
    uid = Column(String(8), ForeignKey("badge.uid", ondelete="CASCADE"), nullable=False)

    equipement = relationship("Equipement", back_populates="logs")
    badge = relationship("Badge", back_populates="logs")

class EDTSalle(Base):
    __tablename__ = "edtsalle"

    id = Column(Integer, primary_key=True, autoincrement=True)
    horairedebut = Column(DateTime, nullable=False)
    horairefin = Column(DateTime, nullable=False)
    cours = Column(String(20), nullable=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=True)
    id_salle = Column(SmallInteger, ForeignKey("salle.id", ondelete="CASCADE"), nullable=False)
    id_classe = Column(SmallInteger, ForeignKey("classe.id", ondelete="CASCADE"), nullable=True)

    utilisateur = relationship("Utilisateur", back_populates="edtsalle")
    salle = relationship("Salle", back_populates="edtsalle")
    classe = relationship("Classe", back_populates="edtsalle")
    reservations = relationship("Reservation", back_populates="edtsalle", cascade="all, delete")

class EDTUtilisateur(Base):
    __tablename__ = "edtutilisateur"

    id = Column(Integer, primary_key=True, autoincrement=True)
    horairedebut = Column(DateTime, nullable=False)
    horairefin = Column(DateTime, nullable=False)
    cours = Column(String(20), nullable=True)
    id_classe = Column(Integer, ForeignKey("classe.id", ondelete="CASCADE"), nullable=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)
    id_salle = Column(SmallInteger, ForeignKey("salle.id", ondelete="CASCADE"), nullable=False)

    classe = relationship("Classe", back_populates="edtutilisateur")
    utilisateur = relationship("Utilisateur", back_populates="edtutilisateur")
    salle = relationship("Salle", back_populates="edtutilisateur")
    absences = relationship("Absence", back_populates="edtutilisateur", cascade="all, delete")
    retards = relationship("Retard", back_populates="edtutilisateur", cascade="all, delete")

class Absence(Base):
    __tablename__ = "absence"

    id = Column(Integer, primary_key=True, autoincrement=True)
    motif = Column(String(50), nullable=True)
    justifiee = Column(Boolean, nullable=False, default=False)
    valide = Column(Boolean, nullable=False, default=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)
    id_edtutilisateur = Column(Integer, ForeignKey("edtutilisateur.id", ondelete="CASCADE"), nullable=False)

    utilisateur = relationship("Utilisateur", back_populates="absences")
    edtutilisateur = relationship("EDTUtilisateur", back_populates="absences")

class Retard(Base):
    __tablename__ = "retard"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duree = Column(Integer, nullable=False)
    motif = Column(String(50), nullable=True)
    justifiee = Column(Boolean, nullable=False, default=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)
    id_edtutilisateur = Column(Integer, ForeignKey("edtutilisateur.id", ondelete="CASCADE"), nullable=False)

    utilisateur = relationship("Utilisateur", back_populates="retards")
    edtutilisateur = relationship("EDTUtilisateur", back_populates="retards")

class EDTClasse(Base):
    __tablename__ = "edtclasse"

    id = Column(Integer, primary_key=True, autoincrement=True)
    horairedebut = Column(DateTime, nullable=False)
    horairefin = Column(DateTime, nullable=False)
    cours = Column(String(20), nullable=True)
    id_classe = Column(Integer, ForeignKey("classe.id", ondelete="CASCADE"), nullable=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=True)
    id_salle = Column(SmallInteger, ForeignKey("salle.id", ondelete="CASCADE"), nullable=False)

    classe = relationship("Classe", back_populates="edtclasse")
    utilisateur = relationship("Utilisateur", back_populates="edtclasse")
    salle = relationship("Salle", back_populates="edtclasse")

class Autorisation(Base):
    __tablename__ = "autorisation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    autorisee = Column(Boolean, nullable=False, default=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)
    id_salle = Column(SmallInteger, ForeignKey("salle.id", ondelete="CASCADE"), nullable=False)

    utilisateur = relationship("Utilisateur", back_populates="autorisations")
    salle = relationship("Salle", back_populates="autorisations")

class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    horairedebut = Column(DateTime, nullable=False)
    horairefin = Column(DateTime, nullable=False)
    id_salle = Column(Integer, ForeignKey("salle.id", ondelete="CASCADE"), nullable=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)
    id_edtsalle = Column(Integer, ForeignKey("edtsalle.id", ondelete="CASCADE"), nullable=False)
    id_classe = Column(Integer, ForeignKey("classe.id", ondelete="CASCADE"), nullable=False)

    edtsalle = relationship("EDTSalle", back_populates="reservations")
    salle = relationship("Salle", back_populates="reservations")
    utilisateur = relationship("Utilisateur", back_populates="reservations")
    classe = relationship("Classe", back_populates="reservations")
