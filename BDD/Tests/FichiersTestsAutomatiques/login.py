import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock, patch
from routes.psw import login
from schemas import LoginRequest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from mocks import MockUtilisateur

# T3.1 – Utilisateur inconnu
def test_login_utilisateur_introuvable():
    db = MagicMock()
    db.query().filter().first.return_value = None

    request = LoginRequest(identifiant="admin123", mot_de_passe="toto123")

    with pytest.raises(HTTPException) as e:
        login(request, db)

    assert e.value.status_code == 404
    assert e.value.detail == "Utilisateur introuvable"

# T3.2 – Mauvais mot de passe
@patch("routes.psw.chiffrement.decryptPassword")
def test_login_mauvais_mot_de_passe(mock_decrypt):
    utilisateur = MockUtilisateur(
        id=1,
        identifiant="admin123",
        mot_de_passe="chiffre_fake",
        nom="Admin",
        prenom="Root",
        role="Admin",
        digicode="0000",
        date_de_naissance="2000-01-01",
        id_classe=None
    )

    db = MagicMock()
    db.query().filter().first.return_value = utilisateur

    mock_decrypt.return_value = "bonmotdepasse"

    request = LoginRequest(identifiant="admin123", mot_de_passe="mauvais")

    with pytest.raises(HTTPException) as e:
        login(request, db)

    assert e.value.status_code == 401
    assert e.value.detail == "Mot de passe incorrect"

# T3.3 – Connexion réussie
@patch("routes.psw.chiffrement.decryptPassword")
def test_login_connexion_reussie(mock_decrypt):
    utilisateur = MockUtilisateur(
        id=1,
        identifiant="admin123",
        mot_de_passe="chiffre_fake",
        nom="Admin",
        prenom="Root",
        role="Admin",
        digicode="0000",
        date_de_naissance="2000-01-01",
        id_classe=None
    )

    db = MagicMock()
    db.query().filter().first.return_value = utilisateur

    mock_decrypt.return_value = "toto123"

    request = LoginRequest(identifiant="admin123", mot_de_passe="toto123")

    result = login(request, db)

    assert result["success"] is True
    assert result["id_utilisateur"] == 1
    assert result["role"] == "Admin"
