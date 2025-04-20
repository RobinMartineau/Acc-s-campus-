import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from unittest.mock import MagicMock
from schemas import AppelRequest
from routes.bae import faireAppel

#Mocks simples pour les modèles
class MockEquipement:
    def __init__(self, adresse_mac, type, id_salle=None, id=1):
        self.adresse_mac = adresse_mac
        self.type = type
        self.id_salle = id_salle
        self.id = id

class MockBadge:
    def __init__(self, uid, id_utilisateur=None, actif=True):
        self.uid = uid
        self.id_utilisateur = id_utilisateur
        self.actif = actif

class MockUtilisateur:
    def __init__(self, id, role="eleve", nom="Dupont", prenom="Jean", id_classe=1):
        self.id = id
        self.role = role
        self.nom = nom
        self.prenom = prenom
        self.id_classe = id_classe

class MockCours:
    def __init__(self, id, horairedebut=None, horairefin=None, id_salle=1):
        self.id = id
        self.horairedebut = horairedebut or datetime.now()
        self.horairefin = horairefin or (self.horairedebut + timedelta(minutes=45))
        self.id_salle = id_salle

class MockClasse:
    def __init__(self, nom):
        self.nom = nom
        self.id = id
        
class MockSalle:
    def __init__(self, id, numero="B202"):
        self.id = id
        self.numero = numero

#T2.1 - MAC inconnue
def test_appel_equipement_introuvable():
    db = MagicMock()
    db.query().filter().first.return_value = None
    req = AppelRequest(uid="123", adresse_mac="00:11:22:33:44")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404
    assert "Équipement introuvable" in exc.value.detail

#T2.2 - Type PEA
def test_appel_type_pea_refuse():
    db = MagicMock()
    db.query().filter().first.side_effect = [MockEquipement("00:11", "PEA")]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 400
    assert "Mauvaise requête" in exc.value.detail

#T2.3 - Badge inconnu
def test_appel_badge_inconnu():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "BAE", 1),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404

#T2.4 - Badge non associé à un utilisateur
def test_appel_badge_non_associe():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "BAE", 1),
        MockBadge("123", None)
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404

#T2.5 - Utilisateur inexistant
def test_appel_utilisateur_inexistant():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "BAE", 1),
        MockBadge("123", 1),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404

#T2.6 - Badge désactivé
def test_appel_badge_desactive():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "BAE", 1),
        MockBadge("123", 1, actif=False),
        MockUtilisateur(1)
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 403

#T2.7 - Équipement sans salle
def test_appel_equipement_sans_salle():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "BAE", id_salle=None),
        MockBadge("123", 1),
        MockUtilisateur(1)
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404

#T2.8 - L'utilisateur n'est pas un élève
def test_appel_utilisateur_pas_eleve():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "BAE", 1),
        MockBadge("123", 1),
        MockUtilisateur(1, role="admin"),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 403

#T2.9 - Aucun cours en ce moment
def test_appel_aucun_cours():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "BAE", 1),
        MockBadge("123", 1),
        MockUtilisateur(1),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 403

#T2.10 - Cours trouvé mais dans une autre salle
def test_appel_cours_dans_autre_salle():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "BAE", 1),
        MockBadge("123", 1),
        MockUtilisateur(1),
        MockCours(2),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 403

#T2.11 - Appel réussi AVEC retard
def test_appel_succes_avec_retard():
    db = MagicMock()

    utilisateur = MockUtilisateur(1, "Eleve")
    badge = MockBadge("123", id_utilisateur=1)
    equipement = MockEquipement("00:11", "BAE", id_salle=1)
    edt = MockCours(1, datetime.now() - timedelta(minutes=10), datetime.now() + timedelta(minutes=50))
    classe = MockClasse("CIEL")
    salle = MockSalle(1)

    db.query().filter().first.side_effect = [
        equipement,
        badge,
        utilisateur,
        salle,
        edt,
        classe
    ]

    req = AppelRequest(uid="123", adresse_mac="00:11")
    response = faireAppel(req, db)

    assert response["nom"] == utilisateur.nom
    assert response["prenom"] == utilisateur.prenom
    assert response["classe"] == "CIEL"

#T2.12 - Appel réussi SANS retard
def test_appel_succes_sans_retard():
    db = MagicMock()

    utilisateur = MockUtilisateur(1, "Eleve")
    badge = MockBadge("123", id_utilisateur=1)
    equipement = MockEquipement("00:11", "BAE", id_salle=1)
    edt = MockCours(1, datetime.now(), datetime.now() + timedelta(minutes=50))
    classe = MockClasse("CIEL")
    salle = MockSalle(1)

    db.query().filter().first.side_effect = [
        equipement,
        badge,
        utilisateur,
        salle,
        edt,
        classe
    ]

    req = AppelRequest(uid="123", adresse_mac="00:11")
    response = faireAppel(req, db)

    assert response["nom"] == utilisateur.nom
    assert response["prenom"] == utilisateur.prenom
    assert response["classe"] == "CIEL"