import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.badge import deleteBadge
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockBadge, MockLog

# T9.1 – UID inexistant
def test_uid_inexistant():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as exc:
        deleteBadge(uid="A1B2C3D4", db=db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Badge non trouvé"

# T9.2 – UID existant, suppression réussie sans logs
def test_uid_existant_suppression_reussie():
    db = MagicMock()
    badge = MockBadge("A1B2C3D4", True, None, 1)
    db.query().filter().first.return_value = badge

    response = deleteBadge(uid="A1B2C3D4", db=db)

    db.delete.assert_called_once_with(badge)
    db.commit.assert_called_once()
    assert response is None

# T9.3 – UID existant avec des logs en base, suppression réussie
def test_uid_existant_avec_logs():
    db = MagicMock()
    badge = MockBadge("A1B2C3D4", True, None, 1)
    log1 = MockLog(1, None, 1, "A1B2C3D4")
    log2 = MockLog(2, None, 1, "A1B2C3D4")

    db.query().filter().first.return_value = badge
    db.query().filter().all.return_value = [log1, log2]

    response = deleteBadge(uid="A1B2C3D4", db=db)

    db.delete.assert_called_once_with(badge)
    db.commit.assert_called_once()
    assert response is None
