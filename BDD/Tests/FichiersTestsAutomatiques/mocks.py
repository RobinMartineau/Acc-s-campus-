#Mock pour les salles
class MockSalle:
    def __init__(self, id, numero, statut):
        self.id = id
        self.numero = numero
        self.statut = statut

#Mock pour les classes
class MockClasse:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom

#Mock pour les équipements
class MockEquipement:
    def __init__(self, id, adresse_mac, type, id_salle):
        self.id = id
        self.adresse_mac = adresse_mac
        self.type = type
        self.id_salle = id_salle

#Mock pour les utilisateurs
class MockUtilisateur:
    def __init__(self, id, identifiant, mot_de_passe, nom, prenom, role, digicode, date_de_naissance, id_classe):
        self.id = id
        self.identifiant = identifiant
        self.mot_de_passe = mot_de_passe
        self.nom = nom
        self.prenom = prenom
        self.role = role
        self.digicode = digicode
        self.date_de_naissance = date_de_naissance
        self.id_classe = id_classe

#Mock pour les badges
class MockBadge:
    def __init__(self, uid, actif, creation, id_utilisateur):
        self.uid = uid
        self.actif = actif
        self.creation = creation
        self.id_utilisateur = id_utilisateur

#Mock pour les logs
class MockLog:
    def __init__(self, id, horaire, id_equipement, uid):
        self.id = id
        self.horaire = horaire
        self.id_equipement = id_equipement
        self.uid = uid

#Mock pour les cours d’une salle (EDTSalle)
class MockEDTSalle:
    def __init__(self, id, horairedebut, horairefin, cours, id_utilisateur, id_classe, id_salle):
        self.id = id
        self.horairedebut = horairedebut
        self.horairefin = horairefin
        self.cours = cours
        self.id_utilisateur = id_utilisateur
        self.id_classe = id_classe
        self.id_salle = id_salle

#Mock pour les cours d’un utilisateur (EDTUtilisateur)
class MockEDTUtilisateur:
    def __init__(self, id, horairedebut, horairefin, cours, id_salle, id_classe, id_utilisateur):
        self.id = id
        self.horairedebut = horairedebut
        self.horairefin = horairefin
        self.cours = cours
        self.id_salle = id_salle
        self.id_classe = id_classe
        self.id_utilisateur = id_utilisateur

#Mock pour les absences
class MockAbsence:
    def __init__(self, id, valide, motif, justifiee, id_utilisateur, id_edt_utilisateur):
        self.id = id
        self.valide = valide
        self.motif = motif
        self.justifiee = justifiee
        self.id_utilisateur = id_utilisateur
        self.id_edt_utilisateur = id_edt_utilisateur

#Mock pour les retards
class MockRetard:
    def __init__(self, id, duree, motif, justifiee, id_utilisateur, id_edt_utilisateur):
        self.id = id
        self.duree = duree
        self.motif = motif
        self.justifiee = justifiee
        self.id_utilisateur = id_utilisateur
        self.id_edt_utilisateur = id_edt_utilisateur

#Mock pour les cours d’une classe (EDTClasse)
class MockEDTClasse:
    def __init__(self, id, horairedebut, horairefin, cours, id_utilisateur, id_salle, id_classe):
        self.id = id
        self.horairedebut = horairedebut
        self.horairefin = horairefin
        self.cours = cours
        self.id_utilisateur = id_utilisateur
        self.id_salle = id_salle
        self.id_classe = id_classe

#Mock pour les autorisations
class MockAutorisation:
    def __init__(self, id, autorisee, id_utilisateur, id_salle):
        self.id = id
        self.autorisee = autorisee
        self.id_utilisateur = id_utilisateur
        self.id_salle = id_salle

#Mock pour les réservations
class MockReservation:
    def __init__(self, id, horairedebut, horairefin, id_edtsalle, id_utilisateur, id_salle, id_classe):
        self.id = id
        self.horairedebut = horairedebut
        self.horairefin = horairefin
        self.id_edtsalle = id_edtsalle
        self.id_utilisateur = id_utilisateur
        self.id_salle = id_salle
        self.id_classe = id_classe
