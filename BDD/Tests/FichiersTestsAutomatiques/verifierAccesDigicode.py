import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from schemas import AccesRequestD
from routes.pea import verifierAccesDigicode

#Mocks simples
class MockEquipement:
    def __init__(self, id=1, type="PEA", id_salle=1):
        self.id = id
        self.type = type
        self.id_salle = id_salle

class MockUtilisateur:
    def __init__(self, id=1, nom="Dupont", prenom="Jean", role="Eleve"):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.role = role

class MockBadge:
    def __init__(self, id_utilisateur=1, actif=True, uid="badge123"):
        self.id_utilisateur = id_utilisateur
        self.actif = actif
        self.uid = uid

class MockAutorisation:
    def __init__(self, autorisee=True):
        self.autorisee = autorisee

class MockCours:
    pass


#T16.1 – Équipement introuvable
def test_01_equipement_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [None]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 404
    assert "Équipement introuvable" in exc.value.detail


#T16.2 – Mauvais type d’équipement
def test_02_type_bae():
    db = MagicMock()
    db.query().filter().first.side_effect = [MockEquipement(type="BAE")]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 400
    assert "contacter un administrateur" in exc.value.detail


#T16.3 – Utilisateur introuvable
def test_03_utilisateur_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(), None
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 404
    assert "Utilisateur inconnu" in exc.value.detail


#T16.4 – Aucun badge associé
def test_04_aucun_badge():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(),
        MockUtilisateur(),
        None
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 404
    assert "Aucun badge associé" in exc.value.detail


#T16.5 – Badge désactivé
def test_05_badge_desactive():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(),
        MockUtilisateur(),
        MockBadge(actif=False)
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 403
    assert "Badge désactivé" in exc.value.detail


#T16.6 – Salle introuvable
def test_06_salle_introuvable():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(id_salle=None),
        MockUtilisateur(),
        MockBadge()
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 404
    assert "Salle non trouvée" in exc.value.detail


#T16.7 – Accès refusé
def test_07_acces_refuse():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(),
        MockUtilisateur(),
        MockBadge(),
        None,
        None
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    with pytest.raises(HTTPException) as exc:
        verifierAccesDigicode(req, db)
    assert exc.value.status_code == 403
    assert "Accès refusé" in exc.value.detail


#T16.8 – Accès autorisé via autorisation
def test_08_acces_autorisation():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(),
        MockUtilisateur(),
        MockBadge(),
        MockAutorisation(autorisee=True),
        None
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    res = verifierAccesDigicode(req, db)
    assert res["nom"] == "Dupont"
    assert res["prenom"] == "Jean"
    assert res["role"] == "Eleve"
    assert res["autorisee"] is True


#T16.9 – Accès autorisé via cours
def test_09_acces_cours():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockEquipement(),
        MockUtilisateur(),
        MockBadge(),
        None,
        MockCours()
    ]

    req = AccesRequestD(digicode="123456", adresse_mac="00:11:22:33:44:55")

    res = verifierAccesDigicode(req, db)
    assert res["nom"] == "Dupont"
    assert res["prenom"] == "Jean"
    assert res["role"] == "Eleve"
    assert res["autorisee"] is True
