import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.pgs import dissocierBadge
from schemas import AssoRequest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockUtilisateur, MockBadge

# T12.1 – Utilisateur inexistant
def test_dissocier_utilisateur_inexistant():
    db = MagicMock()
    db.query().filter().first.side_effect = [None]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    with pytest.raises(HTTPException) as e:
        dissocierBadge(req, db)

    assert e.value.status_code == 404
    assert e.value.detail == "Utilisateur non trouvé"

# T12.2 – Badge inexistant
def test_dissocier_badge_inexistant():
    db = MagicMock()
    utilisateur = MockUtilisateur(2, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    db.query().filter().first.side_effect = [utilisateur, None]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    with pytest.raises(HTTPException) as e:
        dissocierBadge(req, db)

    assert e.value.status_code == 404
    assert e.value.detail == "Badge non trouvé"

# T12.3 – Badge non attribué
def test_dissocier_badge_non_attribue():
    db = MagicMock()
    utilisateur = MockUtilisateur(2, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    badge = MockBadge("123ABC45", True, "2025-03-31", None)

    db.query().filter().first.side_effect = [utilisateur, badge]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    with pytest.raises(HTTPException) as e:
        dissocierBadge(req, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Ce badge n'est pas déjà attribué à un utilisateur"

# T12.4 – Badge attribué à un autre utilisateur
def test_dissocier_badge_autre_utilisateur():
    db = MagicMock()
    utilisateur = MockUtilisateur(2, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    badge = MockBadge("123ABC45", True, "2025-03-31", 3)

    db.query().filter().first.side_effect = [utilisateur, badge]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    with pytest.raises(HTTPException) as e:
        dissocierBadge(req, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Ce badge est attribué à un autre utilisateur"

# T12.5 – Dissociation réussie
def test_dissocier_succes():
    db = MagicMock()
    utilisateur = MockUtilisateur(2, "id", "mdp", "Jean", "Dupont", "eleve", None, None, None)
    badge = MockBadge("123ABC45", True, "2025-03-31", 2)

    db.query().filter().first.side_effect = [utilisateur, badge]
    db.refresh = MagicMock()

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    response = dissocierBadge(req, db)

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(badge)
    assert response.uid == "123ABC45"
    assert response.id_utilisateur is None
