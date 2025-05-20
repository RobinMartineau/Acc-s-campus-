import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.psw import getUAbsence
import datetime
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockEDTUtilisateur, MockAbsence

# T4.1 – Aucun cours passé
def test_get_uabsence_aucun_cours_passe():
    db = MagicMock()
    db.query().filter().all.return_value = []

    with pytest.raises(HTTPException) as e:
        getUAbsence(id_utilisateur=1, db=db)

    assert e.value.status_code == 404
    assert e.value.detail == "Absences non trouvées"

# T4.2 – Cours passés mais aucune absence
def test_get_uabsence_aucune_absence():
    db = MagicMock()

    mock_cours = [
        MockEDTUtilisateur(
            id=10,
            horairedebut=datetime.datetime(2025, 3, 31, 8, 0),
            horairefin=datetime.datetime(2025, 3, 31, 10, 0),
            cours="Mathématiques",
            id_utilisateur=1,
            id_salle=1,
            id_classe=1
        )
    ]

    db.query().filter().all.side_effect = [mock_cours, []]

    with pytest.raises(HTTPException) as e:
        getUAbsence(id_utilisateur=1, db=db)

    assert e.value.status_code == 404
    assert e.value.detail == "Absences non trouvées"

# T4.3 – Absences valides présentes
def test_get_uabsence_succes():
    db = MagicMock()

    mock_cours = [
        MockEDTUtilisateur(
            id=10,
            horairedebut=datetime.datetime(2025, 3, 31, 8, 0),
            horairefin=datetime.datetime(2025, 3, 31, 10, 0),
            cours="Mathématiques",
            id_utilisateur=1,
            id_salle=1,
            id_classe=1
        )
    ]

    mock_absences = [
        MockAbsence(
            id=1,
            valide=True,
            motif="Maladie",
            justifiee=True,
            id_utilisateur=1,
            id_edt_utilisateur=10
        )
    ]

    db.query().filter().all.side_effect = [mock_cours, mock_absences]

    result = getUAbsence(id_utilisateur=1, db=db)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["cours"] == "Mathématiques"
    assert result[0]["justifiee"] is True
    assert result[0]["motif"] == "Maladie"
    assert result[0]["horaire"] == mock_cours[0].horairedebut
