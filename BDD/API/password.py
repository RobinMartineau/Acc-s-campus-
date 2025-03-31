from cryptography.fernet import Fernet
import random
import string
import chiffrement

#Fonction pour générer un mot de passe
def generatePassword():
    voyelles = "aeiouy"
    consonnes = "bcdfghjklmnpqrstvwxz"

    #Génère une majuscule au début du mot de passe
    debut = random.choice(string.ascii_uppercase)

    #Générer le milieu du mot de passe
    milieu = "".join(random.choice(voyelles) + random.choice(consonnes) for _ in range(2))
    milieu_fin = random.choice(voyelles)
    
    #Générer deux chiffres à la fin du mot de passe
    fin = "".join(random.choices(string.digits, k=2))

    #Chiffre le mot de passe
    password = chiffrement.encryptPassword(debut + milieu + milieu_fin + fin)

    return password