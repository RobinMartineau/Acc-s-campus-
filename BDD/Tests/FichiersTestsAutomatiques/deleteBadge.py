from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.badge import deleteBadge

#Mocks
class MockBadge:
    def __init__(self, uid):
        self.uid = uid

class MockLog:
    def __init__(self, uid):
        self.uid = uid

# T9.1 – UID inexistant
def test_uid_inexistant():
    db = MagicMock()
    db.query().filter().first.return_value = None

    try:
        deleteBadge(uid="A1B2C3D4", db=db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Badge non trouvé"

# T9.2 – UID existant, suppression réussie sans logs
def test_uid_existant_suppression_reussie():
    db = MagicMock()
    badge = MockBadge(uid="A1B2C3D4")
    db.query().filter().first.return_value = badge

    response = deleteBadge(uid="A1B2C3D4", db=db)

    db.delete.assert_called_once_with(badge)
    db.commit.assert_called_once()
    assert response is None


# T9.3 – UID existant avec des logs en base, suppression réussie
def test_uid_existant_avec_logs():
    db = MagicMock()
    badge = MockBadge(uid="A1B2C3D4")
    log1 = MockLog(uid="A1B2C3D4")
    log2 = MockLog(uid="A1B2C3D4")

    # Simuler que le badge existe
    db.query().filter().first.return_value = badge

    # Simuler que des logs liés existent (même si la fonction ne les consulte pas)
    db.query().filter().all.return_value = [log1, log2]

    response = deleteBadge(uid="A1B2C3D4", db=db)

    db.delete.assert_called_once_with(badge)
    db.commit.assert_called_once()
    assert response is None
