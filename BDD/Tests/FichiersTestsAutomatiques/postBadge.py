import pytest
import datetime
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.badge import postBadge
from schemas import BadgeCreate

# T8.1 – UID déjà existant
def test_post_badge_uid_deja_existant():
    db = MagicMock()
    db.query().filter().first.return_value = True

    badge_data = BadgeCreate(uid="A1B2C3D4", actif=True, id_utilisateur=5)

    with pytest.raises(HTTPException) as e:
        postBadge(badge_data, db)

    assert e.value.status_code == 400
    assert e.value.detail == "Badge déjà enregistré"

# T8.2 – Création réussie
def test_post_badge_creation_reussie():
    db = MagicMock()
    db.query().filter().first.return_value = None

    # On simule une instance SQLAlchemy fraîche
    badge_mock = MagicMock()
    db.refresh.side_effect = lambda b: b
    db.add.side_effect = lambda b: setattr(b, "creation", datetime.date.today())

    badge_data = BadgeCreate(uid="N4M5L6K7", actif=False, id_utilisateur=3)

    result = postBadge(badge_data, db)

    assert result.uid == "N4M5L6K7"
    assert result.actif is False
    assert result.id_utilisateur == 3
    assert result.creation == datetime.date.today()
