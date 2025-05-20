import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from schemas import AssoRequest
from routes.pgs import associerBadge
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockUtilisateur, MockBadge

# T11.1 – Utilisateur inexistant
def test_utilisateur_inexistant():
    db = MagicMock()
    db.query().filter().first.side_effect = [None]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    with pytest.raises(HTTPException) as e:
        associerBadge(req, db)

    assert e.value.status_code == 404
    assert e.value.detail == "Utilisateur non trouvé"

# T11.2 – Badge inexistant
def test_badge_inexistant():
    db = MagicMock()
    utilisateur = MockUtilisateur(2, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    db.query().filter().first.side_effect = [utilisateur, None]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    with pytest.raises(HTTPException) as e:
        associerBadge(req, db)

    assert e.value.status_code == 404
    assert e.value.detail == "Badge non trouvé"

# T11.3 – Badge déjà attribué
def test_badge_deja_attribue():
    db = MagicMock()
    utilisateur = MockUtilisateur(2, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    badge = MockBadge("123ABC45", True, None, 5)
    db.query().filter().first.side_effect = [utilisateur, badge]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    with pytest.raises(HTTPException) as e:
        associerBadge(req, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Ce badge est déjà attribué à un utilisateur"

# T11.4 – Utilisateur a déjà un badge
def test_utilisateur_a_deja_badge():
    db = MagicMock()
    utilisateur = MockUtilisateur(2, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    badge = MockBadge("123ABC45", True, None, None)
    badge_exist = MockBadge("AUTREBADGE", True, None, 2)

    db.query().filter().first.side_effect = [utilisateur, badge, badge_exist]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    with pytest.raises(HTTPException) as e:
        associerBadge(req, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Cet utilisateur possède déjà un badge"

# T11.5 – Association réussie
def test_association_succes():
    db = MagicMock()
    utilisateur = MockUtilisateur(2, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    badge = MockBadge("123ABC45", True, None, None)

    db.query().filter().first.side_effect = [utilisateur, badge, None]
    db.refresh = MagicMock()

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    response = associerBadge(req, db)

    assert response.uid == "123ABC45"
    assert response.id_utilisateur == 2
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(badge)
