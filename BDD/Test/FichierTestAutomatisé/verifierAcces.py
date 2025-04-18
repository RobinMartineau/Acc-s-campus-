import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from schemas import AccesRequest
from routes.pea import verifierAcces

# Mocks simples pour les modèles
class MockEquipement:
    def __init__(self, adresse_mac, type, id_salle=None, id=1):
        self.id = id
        self.adresse_mac = adresse_mac
        self.type = type
        self.id_salle = id_salle

class MockBadge:
    def __init__(self, uid, id_utilisateur=None, actif=True):
        self.uid = uid
        self.id_utilisateur = id_utilisateur
        self.actif = actif

class MockUtilisateur:
    def __init__(self, id, nom="Doe", prenom="John", role="eleve"):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.role = role

class MockAutorisation:
    def __init__(self, autorisee=True):
        self.autorisee = autorisee

class MockEDTUtilisateur:
    def __init__(self):
        pass

#T1 - MAC inconnue
def test_equipement_introuvable():
    db = MagicMock()
    db.query().filter().first.return_value = None
    req = AccesRequest(uid="123", adresse_mac="00:11:22:33:44")
    
    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 404
    assert "Équipement introuvable" in exc.value.detail

#T2 - Type BAE
def test_equipement_bae():
    db = MagicMock()
    db.query().filter().first.side_effect = [MockEquipement("00:11", "BAE")]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 400

#T3 - Badge inconnu
def test_badge_inconnu():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "PEA", 1),
        None  # Badge pas trouvé
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 404
    assert "Badge inconnu ou non associé" in exc.value.detail

#T4 - Badge non lié à un utilisateur
def test_badge_non_associe_a_utilisateur():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "PEA", 1),
        MockBadge("123", id_utilisateur=None)
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 404
    assert "Badge inconnu ou non associé" in exc.value.detail

#T5 - Utilisateur inexistant
def test_utilisateur_inconnu():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "PEA", 1),
        MockBadge("123", 1),
        None  # Utilisateur introuvable
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 404

#T6 - Badge désactivé
def test_badge_desactive():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "PEA", 1),
        MockBadge("123", 1, actif=False),
        MockUtilisateur(1)
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 403

#T7 - Équipement sans salle
def test_salle_introuvable():
    equipement = MockEquipement("00:11", "PEA", id_salle=None)
    db = MagicMock()
    db.query().filter().first.side_effect = [
        equipement,
        MockBadge("123", 1),
        MockUtilisateur(1)
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 404

#T8 - Aucun accès autorisé ni cours
def test_acces_refuse_aucune_autorisation_et_cours():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "PEA", 1),
        MockBadge("123", 1),
        MockUtilisateur(1),
        None,  # Pas d'autorisation
        None   # Pas de cours
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 403

#T9 - Autorisation trouvée mais refusée
def test_autorisation_refusee():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "PEA", 1),
        MockBadge("123", 1),
        MockUtilisateur(1),
        MockAutorisation(False),  # Refusée
        None  # Pas de cours
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    with pytest.raises(HTTPException) as exc:
        verifierAcces(req, db)
    assert exc.value.status_code == 403
    assert "Accès refusé" in exc.value.detail

#T10 - Autorisation acceptée
def test_acces_autorise_par_autorisation():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "PEA", 1),
        MockBadge("123", 1),
        MockUtilisateur(1, "Jean", "Dupont", "eleve"),
        MockAutorisation(True),
        None
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    result = verifierAcces(req, db)
    assert result["nom"] == "Jean"
    assert result["prenom"] == "Dupont"
    assert result["role"] == "eleve"
    assert result["autorisee"] is True

#T11 - Pas d'autorisation mais cours en EDT
def test_acces_autorise_par_edt():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement("00:11", "PEA", 1),
        MockBadge("123", 1),
        MockUtilisateur(1, "Jean", "Dupont", "eleve"),
        None,
        MockEDTUtilisateur()
    ]
    req = AccesRequest(uid="123", adresse_mac="00:11")

    result = verifierAcces(req, db)
    assert result["nom"] == "Jean"
    assert result["prenom"] == "Dupont"
    assert result["role"] == "eleve"
    assert result["autorisee"] is True
