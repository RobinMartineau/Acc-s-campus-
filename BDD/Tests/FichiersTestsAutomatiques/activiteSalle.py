import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime, timedelta
from routes.psw import activiteSalle
import models as models

#Mocks simples pour les modèles
class MockSalle:
    def __init__(self, id=1):
        self.id = id

class MockEDTSalle:
    def __init__(self, id=23, id_salle=1, horairedebut=None, horairefin=None, cours="Maths", id_utilisateur=12):
        self.id = id
        self.id_salle = id_salle
        self.horairedebut = horairedebut or datetime.now()
        self.horairefin = horairefin or (datetime.now() + timedelta(hours=1))
        self.cours = cours
        self.id_utilisateur = id_utilisateur

class MockUtilisateur:
    def __init__(self, id=12, nom="Doe", prenom="John"):
        self.id = id
        self.nom = nom
        self.prenom = prenom

class MockEquipement:
    def __init__(self, id=1, id_salle=1):
        self.id = id
        self.id_salle = id_salle

class MockLog:
    def __init__(self, uid="A1B2", id_equipement=1, horaire=None):
        self.uid = uid
        self.id_equipement = id_equipement
        self.horaire = horaire or datetime.now()

class MockBadge:
    def __init__(self, uid="A1B2", id_utilisateur=12):
        self.uid = uid
        self.id_utilisateur = id_utilisateur

#T15.1 - Salle inexistante
def test_salle_inexistante():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Salle non trouvée" in exc.value.detail

#T15.2 - Aucune réservation
def test_aucune_reservation():
    db = MagicMock()
    db.query().filter().first.return_value = MockSalle()
    db.query().filter().all.return_value = []

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Aucune réservation trouvée" in exc.value.detail

#T151.3 - Réservation sans utilisateur
def test_reservation_sans_utilisateur():
    db = MagicMock()
    db.query().filter().first.return_value = MockSalle()
    db.query().filter().all.return_value = [MockEDTSalle(id_utilisateur=None)]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Réservation sans utilisateur associée (ID réservation" in exc.value.detail

#T15.4 - Utilisateur réservation introuvable
def test_utilisateur_reservation_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [MockSalle(), None]
    db.query().filter().all.return_value = [MockEDTSalle(id=24, id_utilisateur=8)]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Utilisateur (ID 8) introuvable" in exc.value.detail

#T15.5 - Aucun log récent
def test_aucun_log_dans_heure():
    db = MagicMock()
    db.query().filter().first.side_effect = [MockSalle(), MockUtilisateur()]
    db.query().filter().all.side_effect = [[MockEDTSalle()], [MockEquipement()]]
    db.query().join().join().filter().all.return_value = []

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Aucun badge utilisé dans cette salle depuis moins d'une heure" in exc.value.detail

#T15.6 - Badge introuvable
def test_badge_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [MockSalle(), MockUtilisateur(), None]
    db.query().filter().all.side_effect = [[MockEDTSalle()], [MockEquipement()]]
    db.query().join().join().filter().all.return_value = [MockLog()]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Badge UID A1B2 introuvable" in exc.value.detail

#T15.7 - Badge non associé
def test_badge_non_associe():
    db = MagicMock()
    badge = MockBadge(uid="A1B2", id_utilisateur=None)

    db.query().filter().first.side_effect = [MockSalle(), MockUtilisateur(), badge]
    db.query().filter().all.side_effect = [[MockEDTSalle()], [MockEquipement()]]
    db.query().join().join().filter().all.return_value = [MockLog()]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Badge UID A1B2 non associé à un utilisateur" in exc.value.detail

#T15.8 - Utilisateur du badge introuvable
def test_utilisateur_badge_introuvable():
    db = MagicMock()
    badge = MockBadge(uid="A1B2", id_utilisateur=9)

    db.query().filter().first.side_effect = [MockSalle(), MockUtilisateur(), badge, None]
    db.query().filter().all.side_effect = [[MockEDTSalle()], [MockEquipement()]]
    db.query().join().join().filter().all.return_value = [MockLog()]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Utilisateur ID 9 introuvable pour badge UID A1B2" in exc.value.detail

#T15.9 - Aucun utilisateur final
def test_aucun_utilisateur_final():
    db = MagicMock()
    badge = MockBadge(uid="A1B2", id_utilisateur=10)

    db.query().filter().first.side_effect = [MockSalle(), MockUtilisateur(), badge, None]
    db.query().filter().all.side_effect = [[MockEDTSalle()], [MockEquipement()]]
    db.query().join().join().filter().all.return_value = [MockLog()]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Utilisateur ID 10 introuvable pour badge UID A1B2" in exc.value.detail

#T15.10 - Succès complet
def test_succes_complet():
    db = MagicMock()
    utilisateur = MockUtilisateur()
    badge = MockBadge(uid="A1B2", id_utilisateur=12)

    db.query().filter().first.side_effect = [MockSalle(), utilisateur, badge, utilisateur]
    db.query().filter().all.side_effect = [[MockEDTSalle()], [MockEquipement()]]
    db.query().join().join().filter().all.return_value = [MockLog()]

    result = activiteSalle(1, db)
    assert result["nombre_utilisateurs"] == 1
    assert result["utilisateurs_derniere_heure"][0]["id"] == 12
    assert result["reservations"][0]["cours"] == "Maths"
