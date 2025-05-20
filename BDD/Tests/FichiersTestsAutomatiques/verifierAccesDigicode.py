import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from schemas import AccesRequestD
from routes.pea import verifierAccesDigicode
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import (
    MockEquipement,
    MockUtilisateur,
    MockBadge,
    MockAutorisation,
    MockEDTUtilisateur as MockCours,
    MockSalle
)

# T16.1 – Équipement introuvable
def test_equipement_introuvable():
    db = MagicMock()
    db.query().filter().first.return_value = None

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 404

# T16.2 – Type BAE
def test_equipement_bae():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", 1)
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 400

# T16.3 – Utilisateur introuvable
def test_utilisateur_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "PEA", 1),
        None
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 404

# T16.4 – Aucun badge associé
def test_aucun_badge():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "PEA", 1),
        MockUtilisateur(1, None, None, "Dupont", "Jean", "Eleve", None, None, 1),
        None
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 404

# T16.5 – Badge désactivé
def test_badge_desactive():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "PEA", 1),
        MockUtilisateur(1, None, None, "Dupont", "Jean", "Eleve", None, None, 1),
        MockBadge("badge123", False, None, 1)
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 403

# T16.6 – Salle introuvable
def test_salle_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "PEA", None),
        MockUtilisateur(1, None, None, "Dupont", "Jean", "Eleve", None, None, 1),
        MockBadge("badge123", True, None, 1),
        None  # salle absente
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 404

def test_acces_refuse():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "PEA", 1),
        MockUtilisateur(1, None, None, "Dupont", "Jean", "Eleve", None, None, 1),
        MockBadge("badge123", True, None, 1),
        MockSalle(1, "B101", True),
        None,
        None
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)

    assert exc.value.status_code == 403
    assert "Accès refusé" in exc.value.detail


# T16.8 – Accès autorisé via autorisation
def test_acces_autorisation():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "PEA", 1),
        MockUtilisateur(1, None, None, "Dupont", "Jean", "Eleve", None, None, 1),
        MockBadge("badge123", True, None, 1),
        MockAutorisation(1, True, 1, 1),
        None,
        MockSalle(1, "B101", True)
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    res = verifierAccesDigicode(req, db)

    assert res["nom"] == "Dupont"
    assert res["prenom"] == "Jean"
    assert res["role"] == "Eleve"
    assert res["autorisee"] is True

# T16.9 – Accès autorisé via cours
def test_acces_cours():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "PEA", 1),
        MockUtilisateur(1, None, None, "Dupont", "Jean", "Eleve", None, None, 1),
        MockBadge("badge123", True, None, 1),
        MockSalle(1, "B101", True),
        None,
        MockCours(1, "2025-03-31T08:00", "2025-03-31T10:00", "Maths", 1, 1, 1)
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11")
    res = verifierAccesDigicode(req, db)

    assert res["nom"] == "Dupont"
    assert res["prenom"] == "Jean"
    assert res["role"] == "Eleve"
    assert res["autorisee"] is True
