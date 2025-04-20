from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.psw import getURetard
from models import EDTUtilisateur, Retard
import datetime

#T5.1 – Aucun cours passé
def test_get_uretard_aucun_cours_passe():
    db = MagicMock()
    db.query().filter().all.return_value = []

    try:
        getURetard(id_utilisateur=1, db=db)
        assert False, "Devait lever une exception 404 pour cours vide"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Retards non trouvés"

#T5.2 – Cours passés sans retards
def test_get_uretard_aucun_retard():
    db = MagicMock()

    mock_cours = [
        EDTUtilisateur(id=20, id_utilisateur=1, horairedebut=datetime.datetime(2025, 3, 31, 9, 0), 
                       horairefin=datetime.datetime(2025, 3, 31, 10, 0), cours="Physique")
    ]

    db.query().filter().all.side_effect = [mock_cours, []]

    try:
        getURetard(id_utilisateur=1, db=db)
        assert False, "Devait lever une exception 404 pour retard vide"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Retards non trouvés"

#T5.3 – Retards valides présents
def test_get_uretard_succes():
    db = MagicMock()

    mock_cours = [
        EDTUtilisateur(id=20, id_utilisateur=1, horairedebut=datetime.datetime(2025, 3, 31, 9, 0), 
                       horairefin=datetime.datetime(2025, 3, 31, 10, 0), cours="Physique"),
    ]
    mock_retards = [
        Retard(id=1, id_edtutilisateur=20, duree=15, justifiee=False, motif="Transport en retard")
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
