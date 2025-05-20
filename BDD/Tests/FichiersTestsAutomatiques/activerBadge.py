import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from schemas import ActiBadge
from routes.pgs import activerBadge
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockBadge

# T13.1 – Badge inexistant
def test_activer_badge_inexistant():
    db = MagicMock()
    db.query().filter().first.return_value = None

    req = ActiBadge(uid="123ABC45", actif=True)

    with pytest.raises(HTTPException) as exc:
        activerBadge(req, db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Badge non trouvé"

# T13.2 – Badge déjà actif
def test_activer_badge_deja_actif():
    db = MagicMock()
    db.query().filter().first.return_value = MockBadge("123ABC45", True, None, None)

    req = ActiBadge(uid="123ABC45", actif=True)

    with pytest.raises(HTTPException) as exc:
        activerBadge(req, db)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Badge déjà activé."

# T13.3 – Badge déjà désactivé
def test_desactiver_badge_deja_desactive():
    db = MagicMock()
    db.query().filter().first.return_value = MockBadge("123ABC45", False, None, None)

    req = ActiBadge(uid="123ABC45", actif=False)

    with pytest.raises(HTTPException) as exc:
        activerBadge(req, db)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Badge déjà désactivé."

# T13.4 – Activation OK
def test_activer_badge_succes():
    db = MagicMock()
    badge = MockBadge("123ABC45", False, None, None)
    db.query().filter().first.return_value = badge
    db.refresh = MagicMock()

    req = ActiBadge(uid="123ABC45", actif=True)

    response = activerBadge(req, db)

    assert response.actif is True
    assert response.uid == "123ABC45"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(badge)

# T13.5 – Désactivation OK
def test_desactiver_badge_succes():
    db = MagicMock()
    badge = MockBadge("123ABC45", True, None, None)
    db.query().filter().first.return_value = badge
    db.refresh = MagicMock()

    req = ActiBadge(uid="123ABC45", actif=False)

    response = activerBadge(req, db)

    assert response.actif is False
    assert response.uid == "123ABC45"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(badge)
