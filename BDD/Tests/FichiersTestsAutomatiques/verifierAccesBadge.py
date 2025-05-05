import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from schemas import AccesRequestB
from routes.pea import verifierAccesBadge
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import *

#T1.1 - MAC inconnue
def test_equipement_introuvable():
    db = MagicMock()
    db.query().filter().first.return_value = None
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")
    
    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 404
    assert "Équipement introuvable" in exc.value.detail

#T1.2 - Type BAE
def test_equipement_bae():
    db = MagicMock()
    db.query().filter().first.side_effect = [MockEquipement(1, "00:11:22:33:44:55", "BAE", 1)]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 400

#T1.3 - Badge inconnu
def test_badge_inconnu():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        None
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 404
    assert "Badge inconnu ou non associé" in exc.value.detail

#T1.4 - Badge non lié à un utilisateur
def test_badge_non_associe_a_utilisateur():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        MockBadge("12345678", True,  None, None)
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 404
    assert "Badge inconnu ou non associé" in exc.value.detail

#T1.5 - Utilisateur inexistant
def test_utilisateur_inconnu():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        MockBadge("12345678", None,  None, 1),
        None
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 404

#T1.6 - Badge désactivé
def test_badge_desactive():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        MockBadge("12345678", False,  None, 1),
        MockUtilisateur(1, None, None, None, None, None, None, None, None)
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 403

#T1.7 - Équipement sans salle
def test_salle_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        MockBadge("12345678", True,  None, 1),
        MockUtilisateur(1, None, None, None, None, None, None, None, None),
        None
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 404

#T1.8 - Aucun accès autorisé ni cours
def test_acces_refuse_aucune_autorisation_et_cours():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        MockBadge("12345678", True,  None, 1),
        MockUtilisateur(1, None, None, None, None, None, None, None, None),
        MockSalle(1, None, None),
        None,
        None
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 403
    assert "Accès refusé" in exc.value.detail

#T1.9 - Autorisation trouvée mais refusée
def test_autorisation_refusee():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        MockBadge("12345678", True,  None, 1),
        MockUtilisateur(1, None, None, None, None, None, None, None, None),
        MockSalle(1, None, None),
        MockAutorisation(1, False, 1, 1),
        None
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesBadge(req, db)
    assert exc.value.status_code == 403
    assert "Accès refusé" in exc.value.detail

#T1.10 - Autorisation acceptée
def test_acces_autorise_par_autorisation():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        MockBadge("12345678", True,  None, 1),
        MockUtilisateur(1, None, None, "Jean", "Dupont", "eleve", None, None, None),
        MockSalle(1, None, None),
        MockAutorisation(1, True, 1, 1),
        None
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    result = verifierAccesBadge(req, db)
    assert result["nom"] == "Jean"
    assert result["prenom"] == "Dupont"
    assert result["role"] == "eleve"
    assert result["autorisee"] is True

#T1.11 - Pas d'autorisation mais cours en EDT
def test_acces_autorise_par_edt():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11:22:33:44:55", "PEA", 1),
        MockBadge("12345678", True,  None, 1),
        MockUtilisateur(1, None, None, "Jean", "Dupont", "eleve", None, None, None),
        MockSalle(1, None, None),
        None,
        MockEDTUtilisateur(1, None, None, None, None, None, None)
    ]
    req = AccesRequestB(uid="12345678", adresse_mac="00:11:22:33:44:55")

    result = verifierAccesBadge(req, db)
    assert result["nom"] == "Jean"
    assert result["prenom"] == "Dupont"
    assert result["role"] == "eleve"
    assert result["autorisee"] is True
    
