import os
from dotenv import load_dotenv

#Récupérer le chemin absolu de key.env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'key.env'))

#Charger key.env
load_dotenv(dotenv_path=dotenv_path, override=True)
