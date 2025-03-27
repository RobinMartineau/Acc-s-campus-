from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import utilisateur, autorisation, badge, salle, classe, equipement, edt, pea, bae, pgs, psw

app = FastAPI()

#Ajout des routes
app.include_router(utilisateur.router)
app.include_router(autorisation.router)
app.include_router(badge.router)
app.include_router(salle.router)
app.include_router(classe.router)
app.include_router(equipement.router)
app.include_router(edt.router)
app.include_router(pea.router)
app.include_router(bae.router)
app.include_router(pgs.router)
app.include_router(psw.router)

#Temporaire | Autoriser toute les connexions à l'API
app.add_middleware(
	CORSMiddleware,
	allow_origins = ["*"],
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"],
)

#Message de bienvenue
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Campus Accès"}
