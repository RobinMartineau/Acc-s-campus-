import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.psw import getEleve
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockUtilisateur, MockClasse

# T6.1 – Aucun élève présent
def test_get_eleve_aucun_eleve():
    db = MagicMock()
    db.query().filter().all.return_value = []

    with pytest.raises(HTTPException) as e:
        getEleve(db)

    assert e.value.status_code == 404
    assert e.value.detail == "Élèves non trouvés"

# T6.2 – Élèves sans classes liées
def test_get_eleve_classes_non_trouvees():
    db = MagicMock()
    mock_eleves = [
        MockUtilisateur(1, "t.eleve", "mdp", "Eleve", "Test", "Eleve", None, None, 99)
    ]
    db.query().filter().all.side_effect = [mock_eleves, []]

    with pytest.raises(HTTPException) as e:
        getEleve(db)

    assert e.value.status_code == 404
    assert e.value.detail == "Classes non trouvées"

# T6.3 – Élèves avec classes valides
def test_get_eleve_succes():
    db = MagicMock()
    mock_eleves = [
        MockUtilisateur(1, "j.dupont", "mdp", "Jean", "Dupont", "Eleve", None, None, 2),
        MockUtilisateur(2, "l.martin", "mdp", "Léa", "Martin", "Eleve", None, None, 3),
    ]
    mock_classes = [
        MockClasse(2, "CIEL"),
        MockClasse(3, "SNIR")
    ]
    db.query().filter().all.side_effect = [mock_eleves, mock_classes]

    result = getEleve(db)

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["nom"] == "Jean"
    assert result[0]["classe"] == "CIEL"
    assert result[1]["prenom"] == "Martin"
    assert result[1]["classe"] == "SNIR"
