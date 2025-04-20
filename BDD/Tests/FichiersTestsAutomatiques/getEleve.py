from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.psw import getEleve
from models import Utilisateur, Classe

#T6.1 – Aucun élève présent
def test_get_eleve_aucun_eleve():
    db = MagicMock()
    db.query().filter().all.return_value = []

    try:
        getEleve(db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Élèves non trouvés"

#T6.2 – Élèves sans classes liées
def test_get_eleve_classes_non_trouvees():
    db = MagicMock()

    mock_eleve = [
        Utilisateur(id=1, nom="Test", prenom="Eleve", identifiant="t.eleve", role="Eleve", id_classe=99)
    ]
    db.query().filter().all.side_effect = [mock_eleve, []]

    try:
        getEleve(db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Classes non trouvées"

#T6.3 – Élèves avec classes valides
def test_get_eleve_succes():
    db = MagicMock()

    mock_eleve = [
        Utilisateur(id=1, nom="Dupont", prenom="Jean", identifiant="j.dupont", role="Eleve", id_classe=2),
        Utilisateur(id=2, nom="Martin", prenom="Léa", identifiant="l.martin", role="Eleve", id_classe=3),
    ]
    mock_classes = [
        Classe(id=2, nom="CIEL"),
        Classe(id=3, nom="SNIR")
    ]

    db.query().filter().all.side_effect = [mock_eleve, mock_classes]

    result = getEleve(db)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["nom"] == "Dupont"
    assert result[0]["classe"] == "CIEL"
    assert result[1]["prenom"] == "Léa"
    assert result[1]["classe"] == "SNIR"
