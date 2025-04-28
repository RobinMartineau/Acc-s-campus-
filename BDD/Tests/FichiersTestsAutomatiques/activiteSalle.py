import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
import datetime
from routes.psw import activiteSalle


#Mocks
class MockSalle:
    def __init__(self, id=1):
        self.id = id

class MockEDTSalle:
    def __init__(self, id=1, id_utilisateur=1, horairedebut="2025-04-28T08:00", horairefin="2025-04-28T10:00", cours="Maths"):
        self.id = id
        self.id_utilisateur = id_utilisateur
        self.horairedebut = horairedebut
        self.horairefin = horairefin
        self.cours = cours

class MockUtilisateur:
    def __init__(self, id=1, nom="Dupont", prenom="Jean"):
        self.id = id
        self.nom = nom
        self.prenom = prenom

class MockLog:
    def __init__(self, id=1, id_badge="12345678", horaire=None):
        self.id = id
        self.id_badge = id_badge
        if horaire:
            self.horaire = horaire
        else:
            self.horaire = datetime.datetime.now()

class MockBadge:
    def __init__(self, uid="12345678", id_utilisateur=1):
        self.uid = uid
        self.id_utilisateur = id_utilisateur


#T15.1 - Salle inexistante
def test_01_salle_inexistante():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Salle non trouvée" in exc.value.detail


#T15.2 - Aucune réservation
def test_02_aucune_reservation():
    db = MagicMock()
    db.query().filter().first.return_value = MockSalle()
    db.query().filter().all.return_value = []

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Aucune réservation trouvée" in exc.value.detail


#T15.3 - Réservation sans utilisateur
def test_03_reservation_sans_utilisateur():
    db = MagicMock()
    db.query().filter().first.return_value = MockSalle()
    db.query().filter().all.return_value = [MockEDTSalle(id_utilisateur=None)]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Réservation sans utilisateur associée" in exc.value.detail


#T15.4 - Utilisateur réservation introuvable
def test_04_utilisateur_reservation_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(),
        None
    ]
    db.query().filter().all.return_value = [MockEDTSalle()]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Utilisateur introuvable" in exc.value.detail


#T15.5 - Aucun badge récent
def test_05_aucun_badge_recent():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(),
        MockUtilisateur()
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle()],
        []
    ]

    res = activiteSalle(1, db)
    assert res["reservations"] != []
    assert res["utilisateurs_derniere_heure"] == []
    assert res["nombre_utilisateurs"] == 0


#T15.6 - Badge introuvable
def test_06_badge_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(),
        MockUtilisateur(),
        None
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle()],
        [MockLog()]
    ]
    db.query().join().join().filter().all.return_value = [MockLog()]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Badge non trouvé." in exc.value.detail


#T15.7 - Badge non associé
def test_07_badge_non_associe():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(),
        MockUtilisateur(),
        MockBadge(id_utilisateur=None)
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle()],
        [MockLog()]
    ]
    db.query().join().join().filter().all.return_value = [MockLog()]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Badge non associé à un utilisateur." in exc.value.detail


#T15.8 - Utilisateur badge introuvable
def test_08_utilisateur_badge_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(),
        MockUtilisateur(),
        MockBadge(),
        None
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle()],
        [MockLog()]
    ]
    db.query().join().join().filter().all.return_value = [MockLog()]
    
    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Utilisateur du badge non trouvé." in exc.value.detail

#T15.9 - Succès complet
def test_09_succes_complet():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(),
        MockUtilisateur(),
        MockBadge(),
        MockUtilisateur()
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle()],
        [MockLog()]
    ]
    db.query().join().join().filter().all.return_value = [MockLog()]
    
    res = activiteSalle(1, db)
    assert res["reservations"] != []
    assert res["utilisateurs_derniere_heure"] != []
    assert res["nombre_utilisateurs"] == 1
