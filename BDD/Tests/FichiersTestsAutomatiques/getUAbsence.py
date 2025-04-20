from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.psw import getUAbsence
from models import EDTUtilisateur, Absence
import datetime

#T4.1 – Aucun cours passé
def test_get_uabsence_aucun_cours_passe():
    db = MagicMock()
    db.query().filter().all.return_value = []

    try:
        getUAbsence(id_utilisateur=1, db=db)
        assert False, "Devait lever une exception 404 pour cours vide"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Absences non trouvées"

#T4.2 – Cours passés mais aucune absence
def test_get_uabsence_aucune_absence():
    db = MagicMock()

    mock_cours = [
        EDTUtilisateur(id=10, id_utilisateur=1, horairedebut=datetime.datetime(2025, 3, 31, 8, 0), 
                       horairefin=datetime.datetime(2025, 3, 31, 10, 0), cours="Mathématiques")
    ]

    db.query().filter().all.side_effect = [mock_cours, []]

    try:
        getUAbsence(id_utilisateur=1, db=db)
        assert False, "Devait lever une exception 404 pour absence vide"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Absences non trouvées"

#T4.3 – Absences valides présentes
def test_get_uabsence_succes():
    db = MagicMock()

    mock_cours = [
        EDTUtilisateur(id=10, id_utilisateur=1, horairedebut=datetime.datetime(2025, 3, 31, 8, 0), 
                       horairefin=datetime.datetime(2025, 3, 31, 10, 0), cours="Mathématiques"),
    ]
    mock_absences = [
        Absence(id=1, id_edtutilisateur=10, justifiee=True, valide=True, motif="Maladie")
    ]

    db.query().filter().all.side_effect = [mock_cours, mock_absences]

    result = getUAbsence(id_utilisateur=1, db=db)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["cours"] == "Mathématiques"
    assert result[0]["justifiee"] is True
    assert result[0]["motif"] == "Maladie"
    assert result[0]["horaire"] == mock_cours[0].horairedebut
