from fastapi import HTTPException
from unittest.mock import MagicMock
from routes.pgs import getUtilisateurs
from chiffrement import encryptPassword

#Mock du modèle Utilisateur
class MockUtilisateur:
    def __init__(self, id, nom, prenom, identifiant, role, date_de_naissance, mot_de_passe, id_classe, digicode):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.identifiant = identifiant
        self.role = role
        self.date_de_naissance = date_de_naissance
        self.mot_de_passe = mot_de_passe
        self.id_classe = id_classe
        self.digicode = digicode

class MockClasse:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
        
#T10.1 – Aucun utilisateur
def test_get_utilisateurs_aucun_utilisateur():
    db = MagicMock()
    db.query().all.return_value = []

    try:
        getUtilisateurs(db)
        assert False, "Devait lever une exception 404"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Aucun utilisateur"

#T10.2 – Utilisateurs présents
def test_get_utilisateurs_liste_complete():
    db = MagicMock()
    utilisateurs = [
        MockUtilisateur(
            id=1, nom="Dupont", prenom="Jean", identifiant="jean.dupont", role="Eleve",
            date_de_naissance="2005-04-01", mot_de_passe=encryptPassword("Tynego28"),
            id_classe=1, digicode="654321"
        ),
        MockUtilisateur(
            id=2, nom="Marie", prenom="Frank", identifiant="frank.marie", role="Prof",
            date_de_naissance="1976-05-11", mot_de_passe=encryptPassword("Gezaqi71"),
            id_classe=None, digicode="123456"
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


