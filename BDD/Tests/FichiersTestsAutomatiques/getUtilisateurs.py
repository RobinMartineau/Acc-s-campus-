import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.pgs import getUtilisateurs
from chiffrement import encryptPassword
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockUtilisateur, MockClasse

# T10.1 – Aucun utilisateur
def test_get_utilisateurs_aucun_utilisateur():
    db = MagicMock()
    db.query().all.return_value = []

    with pytest.raises(HTTPException) as e:
        getUtilisateurs(db)

    assert e.value.status_code == 404
    assert e.value.detail == "Aucun utilisateur"

# T10.2 – Utilisateurs présents
def test_get_utilisateurs_liste_complete():
    db = MagicMock()
    utilisateurs = [
        MockUtilisateur(
            id=1,
            identifiant="jean.dupont",
            mot_de_passe=encryptPassword("Tynego28"),
            nom="Dupont",
            prenom="Jean",
            role="Eleve",
            digicode="654321",
            date_de_naissance="2005-04-01",
            id_classe=1
        ),
        MockUtilisateur(
            id=2,
            identifiant="frank.marie",
            mot_de_passe=encryptPassword("Gezaqi71"),
            nom="Marie",
            prenom="Frank",
            role="Prof",
            digicode="123456",
            date_de_naissance="1976-05-11",
            id_classe=None
        )
    ]

    db.query.return_value.all.return_value = utilisateurs

    def filter_side_effect(*args, **kwargs):
        if hasattr(args[0].right, 'value') and args[0].right.value == 1:
            mock_filter = MagicMock()
            mock_filter.first.return_value = MockClasse(id=1, nom="CIEL")
            return mock_filter
        else:
            mock_filter = MagicMock()
            mock_filter.first.return_value = None
            return mock_filter

    db.query.return_value.filter.side_effect = filter_side_effect

    response = getUtilisateurs(db=db)

    assert isinstance(response, list)
    assert len(response) == 2

    assert response[0]["id"] == 1
    assert response[0]["mot_de_passe"] == "Tynego28"
    assert response[0]["classe"] == "CIEL"

    assert response[1]["id"] == 2
    assert response[1]["mot_de_passe"] == "Gezaqi71"
    assert response[1]["classe"] is None
