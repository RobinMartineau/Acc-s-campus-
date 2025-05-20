import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
import datetime
from routes.psw import activiteSalle
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockSalle, MockEDTSalle, MockUtilisateur, MockBadge, MockLog

# T15.1 - Salle inexistante
def test_01_salle_inexistante():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Salle non trouvée" in exc.value.detail

# T15.2 - Aucune réservation
def test_02_aucune_reservation():
    db = MagicMock()
    db.query().filter().first.return_value = MockSalle(1, None, None)
    db.query().filter().all.return_value = []

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Aucune réservation trouvée" in exc.value.detail

# T15.3 - Réservation sans utilisateur
def test_03_reservation_sans_utilisateur():
    db = MagicMock()
    db.query().filter().first.return_value = MockSalle(1, None, None)
    db.query().filter().all.return_value = [MockEDTSalle(1, "2025-04-28T08:00", "2025-04-28T10:00", "Maths", None, 1, 1)]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Réservation sans utilisateur associée" in exc.value.detail

# T15.4 - Utilisateur réservation introuvable
def test_04_utilisateur_reservation_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(1, None, None),
        None
    ]
    db.query().filter().all.return_value = [MockEDTSalle(1, "2025-04-28T08:00", "2025-04-28T10:00", "Maths", 1, 1, 1)]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Utilisateur introuvable" in exc.value.detail

# T15.5 - Aucun badge récent
def test_05_aucun_badge_recent():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(1, None, None),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle(1, "2025-04-28T08:00", "2025-04-28T10:00", "Maths", 1, 1, 1)],
        []
    ]

    res = activiteSalle(1, db)
    assert res["reservations"] != []
    assert res["utilisateurs_derniere_heure"] == []
    assert res["nombre_utilisateurs"] == 0

# T15.6 - Badge introuvable
def test_06_badge_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(1, None, None),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None),
        None
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle(1, "2025-04-28T08:00", "2025-04-28T10:00", "Maths", 1, 1, 1)],
        [MockLog(1, datetime.datetime.now(), 1, "12345678")]
    ]
    db.query().join().join().filter().all.return_value = [MockLog(1, datetime.datetime.now(), 1, "12345678")]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Badge non trouvé." in exc.value.detail

# T15.7 - Badge non associé
def test_07_badge_non_associe():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(1, None, None),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None),
        MockBadge("12345678", True, None, None)  # id_utilisateur à None
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle(1, "2025-04-28T08:00", "2025-04-28T10:00", "Maths", 1, 1, 1)],
        [MockLog(1, datetime.datetime.now(), 1, "12345678")]
    ]
    db.query().join().join().filter().all.return_value = [MockLog(1, datetime.datetime.now(), 1, "12345678")]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Badge non associé à un utilisateur." in exc.value.detail

# T15.8 - Utilisateur badge introuvable
def test_08_utilisateur_badge_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(1, None, None),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None),
        MockBadge("12345678", True, None, 1),
        None
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle(1, "2025-04-28T08:00", "2025-04-28T10:00", "Maths", 1, 1, 1)],
        [MockLog(1, datetime.datetime.now(), 1, "12345678")]
    ]
    db.query().join().join().filter().all.return_value = [MockLog(1, datetime.datetime.now(), 1, "12345678")]

    with pytest.raises(HTTPException) as exc:
        activiteSalle(1, db)
    assert exc.value.status_code == 404
    assert "Utilisateur du badge non trouvé." in exc.value.detail

# T15.9 - Succès complet
def test_09_succes_complet():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockSalle(1, None, None),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None),
        MockBadge("12345678", True, None, 1),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    ]
    db.query().filter().all.side_effect = [
        [MockEDTSalle(1, "2025-04-28T08:00", "2025-04-28T10:00", "Maths", 1, 1, 1)],
        [MockLog(1, datetime.datetime.now(), 1, "12345678")]
    ]
    db.query().join().join().filter().all.return_value = [MockLog(1, datetime.datetime.now(), 1, "12345678")]

    res = activiteSalle(1, db)
    assert res["reservations"] != []
    assert res["utilisateurs_derniere_heure"] != []
    assert res["nombre_utilisateurs"] == 1
