from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.badge import deleteBadge

#Mock de l’objet Badge
class MockBadge:
    def __init__(self, uid):
        self.uid = uid

#T9.1 – UID inexistant
def test_uid_inexistant():
    db = MagicMock()
    db.query().filter().first.return_value = None

    try:
        deleteBadge(uid="A1B2C3D4", db=db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Badge non trouvé"

#T9.2 – UID existant, suppression réussie
def test_uid_existant_suppression_reussie():
    db = MagicMock()
    badge = MockBadge(uid="A1B2C3D4")
    db.query().filter().first.return_value = badge

    response = deleteBadge(uid="A1B2C3D4", db=db)

    db.delete.assert_called_once_with(badge)
    db.commit.assert_called_once()
    assert response is None
