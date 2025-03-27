import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv(dotenv_path = "key.env")

# Récupérer la clé depuis le fichier .env
KEY = os.getenv("SECRET_KEY")

if KEY is None:
    raise ValueError("La clé de chiffrement est introuvable. Vérifie ton fichier .env")

cipher_suite = Fernet(KEY.encode())

#Fonction pour chiffrer le mot de passe
def encryptPassword(password: str) -> str:
    return cipher_suite.encrypt(password.encode()).decode()

#Fonction pour déchiffrer le mot de passe
def decryptPassword(encrypted_password: str) -> str:
    return cipher_suite.decrypt(encrypted_password.encode()).decode()
