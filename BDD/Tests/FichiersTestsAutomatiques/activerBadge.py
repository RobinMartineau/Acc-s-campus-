from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.pgs import activerBadge
from schemas import ActiBadge

#Mock modèle Badge
class MockBadge:
    def __init__(self, uid, actif):
        self.uid = uid
        self.actif = actif

#T13.1 – Badge inexistant
def test_activer_badge_inexistant():
    db = MagicMock()
    db.query().filter().first.return_value = None

    req = ActiBadge(uid="123ABC45", actif=True)

    try:
        activerBadge(req, db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Badge non trouvé"

#T13.2 – Badge déjà actif
def test_activer_badge_deja_actif():
    db = MagicMock()
    badge = MockBadge(uid="123ABC45", actif=True)
    db.query().filter().first.return_value = badge

    req = ActiBadge(uid="123ABC45", actif=True)

    try:
        activerBadge(req, db)
        assert False, "Devait lever une exception 403"
    except HTTPException as e:
        assert e.status_code == 403
        assert e.detail == "Badge déjà activé."

#T13.3 – Badge déjà désactivé
def test_desactiver_badge_deja_desactive():
    db = MagicMock()
    badge = MockBadge(uid="123ABC45", actif=False)
    db.query().filter().first.return_value = badge

    req = ActiBadge(uid="123ABC45", actif=False)

    try:
        activerBadge(req, db)
        assert False, "Devait lever une exception 403"
    except HTTPException as e:
        assert e.status_code == 403
        assert e.detail == "Badge déjà désactivé."

#T13.4 – Activation OK
def test_activer_badge_succes():
    db = MagicMock()
    badge = MockBadge(uid="123ABC45", actif=False)
    db.query().filter().first.return_value = badge

    req = ActiBadge(uid="123ABC45", actif=True)
    db.refresh = MagicMock()

    response = activerBadge(req, db)

    assert response.actif == True
    assert response.uid == "123ABC45"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(badge)

#T13.5 – Désactivation OK
def test_desactiver_badge_succes():
    db = MagicMock()
    badge = MockBadge(uid="123ABC45", actif=True)
    db.query().filter().first.return_value = badge

    req = ActiBadge(uid="123ABC45", actif=False)
    db.refresh = MagicMock()

    response = activerBadge(req, db)

    assert response.actif == False
    assert response.uid == "123ABC45"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(badge)
