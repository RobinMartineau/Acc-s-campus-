from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.pgs import dissocierBadge
import schemas

#Mocks simples pour les modèles
class MockBadge:
    def __init__(self, uid, id_utilisateur=None):
        self.uid = uid
        self.id_utilisateur = id_utilisateur
        self.actif = True
        self.creation = "2025-03-31"

class MockUtilisateur:
    def __init__(self, id):
        self.id = id

#T12.1 – Utilisateur inexistant
def test_dissocier_utilisateur_inexistant():
    db = MagicMock()
    db.query().filter().first.side_effect = [None]

    req = schemas.AssoRequest(uid="123ABC45", id_utilisateur=2)

    try:
        dissocierBadge(req, db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Utilisateur non trouvé"

#T12.2 – Badge inexistant
def test_dissocier_badge_inexistant():
    db = MagicMock()
    db.query().filter().first.side_effect = [
        MockUtilisateur(id=2),
        None
    ]

    req = schemas.AssoRequest(uid="123ABC45", id_utilisateur=2)

    try:
        dissocierBadge(req, db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Badge non trouvé"

#T12.3 – Badge non attribué
def test_dissocier_badge_non_attribue():
    db = MagicMock()
    badge = MockBadge(uid="123ABC45", id_utilisateur=None)

    db.query().filter().first.side_effect = [
        MockUtilisateur(id=2),
        badge
    ]

    req = schemas.AssoRequest(uid="123ABC45", id_utilisateur=2)

    try:
        dissocierBadge(req, db)
        assert False, "Devait lever une exception 400"
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Ce badge n'est pas déjà attribué à un utilisateur"

#T12.4 – Badge attribué à un autre utilisateur
def test_dissocier_badge_autre_utilisateur():
    db = MagicMock()
    badge = MockBadge(uid="123ABC45", id_utilisateur=3)

    db.query().filter().first.side_effect = [
        MockUtilisateur(id=2),
        badge
    ]

    req = schemas.AssoRequest(uid="123ABC45", id_utilisateur=2)

    try:
        dissocierBadge(req, db)
        assert False, "Devait lever une exception 400"
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Ce badge est attribué à un autre utilisateur"

#T12.5 – Dissociation réussie
def test_dissocier_succes():
    db = MagicMock()
    badge = MockBadge(uid="123ABC45", id_utilisateur=2)

    db.query().filter().first.side_effect = [
        MockUtilisateur(id=2),
        badge
    ]

    req = schemas.AssoRequest(uid="123ABC45", id_utilisateur=2)

    response = dissocierBadge(req, db)

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(badge)
    assert response.uid == "123ABC45"
    assert response.id_utilisateur is None
