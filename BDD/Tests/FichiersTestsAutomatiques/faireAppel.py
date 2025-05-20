import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from unittest.mock import MagicMock
from schemas import AppelRequest
from routes.bae import faireAppel
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockEquipement, MockBadge, MockUtilisateur, MockSalle, MockEDTClasse, MockClasse

# T2.1 – MAC inconnue
def test_appel_equipement_introuvable():
    db = MagicMock()
    db.query().filter().first.return_value = None
    req = AppelRequest(uid="123", adresse_mac="00:11:22:33:44")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404
    assert "Équipement introuvable" in exc.value.detail

# T2.2 – Type PEA
def test_appel_type_pea_refuse():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "PEA", 1)
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 400
    assert "Mauvaise requête" in exc.value.detail

# T2.3 – Badge inconnu
def test_appel_badge_inconnu():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", 1),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404

# T2.4 – Badge non associé à un utilisateur
def test_appel_badge_non_associe():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", 1),
        MockBadge("123", True, None, None)
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404

# T2.5 – Utilisateur inexistant
def test_appel_utilisateur_inexistant():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", 1),
        MockBadge("123", True, None, 1),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404

# T2.6 – Badge désactivé
def test_appel_badge_desactive():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", 1),
        MockBadge("123", False, None, 1),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, 1)
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 403

# T2.7 – Équipement sans salle
def test_appel_equipement_sans_salle():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", None),
        MockBadge("123", True, None, 1),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, 1)
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 404

# T2.8 – Utilisateur non élève
def test_appel_utilisateur_pas_eleve():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", 1),
        MockBadge("123", True, None, 1),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "admin", None, None, 1),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 403

# T2.9 – Aucun cours
def test_appel_aucun_cours():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", 1),
        MockBadge("123", True, None, 1),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, 1),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 403

# T2.10 – Cours dans une autre salle
def test_appel_cours_dans_autre_salle():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(1, "00:11", "BAE", 1),
        MockBadge("123", True, None, 1),
        MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "eleve", None, None, 1),
        MockEDTClasse(1, datetime.now(), datetime.now() + timedelta(minutes=45), "Maths", 1, 2, 1),
        None
    ]
    req = AppelRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        faireAppel(req, db)
    assert exc.value.status_code == 403

# T2.11 – Succès avec retard
def test_appel_succes_avec_retard():
    db = MagicMock()
    utilisateur = MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "Eleve", None, None, 1)
    badge = MockBadge("123", True, None, 1)
    equipement = MockEquipement(1, "00:11", "BAE", 1)
    edt = MockEDTClasse(1, datetime.now() - timedelta(minutes=10), datetime.now() + timedelta(minutes=50), "Maths", 1, 1, 1)
    salle = MockSalle(1, "B202", "ouverte")
    classe = MockClasse(1, "CIEL")

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

# T2.12 – Succès sans retard
def test_appel_succes_sans_retard():
    db = MagicMock()
    utilisateur = MockUtilisateur(1, "id", "mdp", "Jean", "Dupont", "Eleve", None, None, 1)
    badge = MockBadge("123", True, None, 1)
    equipement = MockEquipement(1, "00:11", "BAE", 1)
    edt = MockEDTClasse(1, datetime.now(), datetime.now() + timedelta(minutes=50), "Maths", 1, 1, 1)
    salle = MockSalle(1, "B202", "ouverte")
    classe = MockClasse(1, "CIEL")

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
