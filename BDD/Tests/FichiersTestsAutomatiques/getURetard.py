import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.psw import getURetard
import datetime
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockEDTUtilisateur, MockRetard

# T5.1 – Aucun cours passé
def test_get_uretard_aucun_cours_passe():
    db = MagicMock()
    db.query().filter().all.return_value = []

    with pytest.raises(HTTPException) as e:
        getURetard(id_utilisateur=1, db=db)

    assert e.value.status_code == 404
    assert e.value.detail == "Retards non trouvés"

# T5.2 – Cours passés sans retards
def test_get_uretard_aucun_retard():
    db = MagicMock()

    mock_cours = [
        MockEDTUtilisateur(
            id=20,
            horairedebut=datetime.datetime(2025, 3, 31, 9, 0),
            horairefin=datetime.datetime(2025, 3, 31, 10, 0),
            cours="Physique",
            id_salle=1,
            id_classe=1,
            id_utilisateur=1
        )
    ]

    db.query().filter().all.side_effect = [mock_cours, []]

    with pytest.raises(HTTPException) as e:
        getURetard(id_utilisateur=1, db=db)

    assert e.value.status_code == 404
    assert e.value.detail == "Retards non trouvés"

# T5.3 – Retards valides présents
def test_get_uretard_succes():
    db = MagicMock()

    mock_cours = [
        MockEDTUtilisateur(
            id=20,
            horairedebut=datetime.datetime(2025, 3, 31, 9, 0),
            horairefin=datetime.datetime(2025, 3, 31, 10, 0),
            cours="Physique",
            id_salle=1,
            id_classe=1,
            id_utilisateur=1
        )
    ]
    mock_retards = [
        MockRetard(
            id=1,
            duree=15,
            motif="Transport en retard",
            justifiee=False,
            id_utilisateur=1,
            id_edt_utilisateur=20
        )
    ]

    db.query().filter().all.side_effect = [mock_cours, mock_retards]

    result = getURetard(id_utilisateur=1, db=db)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["cours"] == "Physique"
    assert result[0]["horaire"] == mock_cours[0].horairedebut
    assert result[0]["duree"] == 15
    assert result[0]["justifiee"] is False
    assert result[0]["motif"] == "Transport en retard"
