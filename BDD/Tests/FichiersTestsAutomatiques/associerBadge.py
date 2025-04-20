from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.pgs import associerBadge
from schemas import AssoRequest

#Mock classes pour Utilisateur et Badge
class MockUtilisateur:
    def __init__(self, id):
        self.id = id

class MockBadge:
    def __init__(self, uid, id_utilisateur=None):
        self.uid = uid
        self.id_utilisateur = id_utilisateur

#T11.1 – Utilisateur inexistant
def test_utilisateur_inexistant():
    db = MagicMock()
    db.query().filter().first.side_effect = [None]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    try:
        associerBadge(req, db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Utilisateur non trouvé"

#T11.2 – Badge inexistant
def test_badge_inexistant():
    db = MagicMock()
    utilisateur = MockUtilisateur(id=2)
    db.query().filter().first.side_effect = [utilisateur, None]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    try:
        associerBadge(req, db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Badge non trouvé"

#T11.3 – Badge déjà attribué
def test_badge_deja_attribue():
    db = MagicMock()
    utilisateur = MockUtilisateur(id=2)
    badge = MockBadge(uid="123ABC45", id_utilisateur=5)
    db.query().filter().first.side_effect = [utilisateur, badge]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    try:
        associerBadge(req, db)
        assert False, "Devait lever une exception 400"
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Ce badge est déjà attribué à un utilisateur"

#T11.4 – Utilisateur a déjà un badge
def test_utilisateur_a_deja_badge():
    db = MagicMock()
    utilisateur = MockUtilisateur(id=2)
    badge = MockBadge(uid="123ABC45", id_utilisateur=None)
    badge_exist = MockBadge(uid="AUTREBADGE", id_utilisateur=2)

    db.query().filter().first.side_effect = [utilisateur, badge, badge_exist]

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    try:
        associerBadge(req, db)
        assert False, "Devait lever une exception 400"
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Cet utilisateur possède déjà un badge"

#T11.5 – Association réussie
def test_association_succes():
    db = MagicMock()
    utilisateur = MockUtilisateur(id=2)
    badge = MockBadge(uid="123ABC45", id_utilisateur=None)

    db.query().filter().first.side_effect = [utilisateur, badge, None]
    db.refresh = MagicMock()

    req = AssoRequest(uid="123ABC45", id_utilisateur=2)

    response = associerBadge(req, db)

    assert response.uid == "123ABC45"
    assert response.id_utilisateur == 2
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(badge)
