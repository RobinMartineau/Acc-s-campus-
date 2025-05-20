import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.salle import getSalles
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockSalle

# T14.1 – Aucune salle en base
def test_get_salles_aucune_salle():
    db = MagicMock()
    db.query().all.return_value = []

    with pytest.raises(HTTPException) as e:
        getSalles(db)

    assert e.value.status_code == 404
    assert e.value.detail == "Salles non trouvées"

# T14.2 – Plusieurs salles présentes
def test_get_salles_liste_presente():
    db = MagicMock()
    salles = [
        MockSalle(1, "B101", True),
        MockSalle(2, "A302", False)
    ]
    db.query().all.return_value = salles

    result = getSalles(db)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0].id == 1
    assert result[0].numero == "B101"
    assert result[0].statut is True

    assert result[1].id == 2
    assert result[1].numero == "A302"
    assert result[1].statut is False
