from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.salle import getSalles
from models import Salle

#T14.1 – Aucune salle en base
def test_get_salles_aucune_salle():
    db = MagicMock()
    db.query().all.return_value = []

    try:
        getSalles(db)
        assert False, "Doit lever une exception 404 si aucune salle trouvée"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Salles non trouvées"

#T14.2 – Plusieurs salles présentes
def test_get_salles_liste_presente():
    salle1 = Salle(id=1, numero="B101", statut=True)
    salle2 = Salle(id=2, numero="A302", statut=False)

    db = MagicMock()
    db.query().all.return_value = [salle1, salle2]

    result = getSalles(db)

    assert isinstance(result, list)
    assert len(result) == 2

    assert result[0].id == 1
    assert result[0].numero == "B101"
    assert result[0].statut is True

    assert result[1].id == 2
    assert result[1].numero == "A302"
    assert result[1].statut is False
