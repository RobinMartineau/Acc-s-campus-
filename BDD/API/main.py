from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routes import utilisateur, autorisation, badge, edt, pea, bae, pgs, psw, reservation, equipement, salle
import ipaddress

app = FastAPI(
    title="API ACCES CAMPUS",
    description="API utiliser pour répondre aux requêtes envoyés par le PGS, le PSW, les BAEs et PEAs.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "BAE",
            "description": "Tout ce qui concerne les BAEs."
        },
        {
            "name": "PEA",
            "description": "Tout ce qui concerne les PEAs."
        },
        {
            "name": "PGS",
            "description": "Tout ce qui concerne le PGS."
        },
        {
            "name": "PSW",
            "description": "Tout ce qui concerne le PSW."
        },
    ]
)

# Middleware IP Filtering
@app.middleware("http")
async def ip_filter_middleware(request: Request, call_next):
    # Vérifier si c'est une méthode POST
    if request.method in {"POST", "DELETE", "PUT"}:
        client_ip = request.client.host

        try:
            ip = ipaddress.ip_address(client_ip)
        except ValueError:
            raise HTTPException(status_code=400, detail="Adresse IP invalide")

        # Définir les sous-réseaux autorisés
        allowed_networks = [
                ipaddress.ip_network('172.20.0.0/16'), #Baronnerie
            ipaddress.ip_network('192.168.4.0/22'), #VLAN 20
            ipaddress.ip_network('192.168.30.0/24'), #VLAN 30
            ipaddress.ip_network('127.0.0.1/32'), #Localhost
        ]

        # Vérifie si l'IP appartient à l'un des réseaux autorisés
        if not any(ip in network for network in allowed_networks):
            raise HTTPException(status_code=403, detail="Accès interdit : IP non autorisée")

    # Continuer la requête
    response = await call_next(request)
    return response


#Ajout des routes
app.include_router(utilisateur.router)
app.include_router(autorisation.router)
app.include_router(badge.router)
app.include_router(edt.router)
app.include_router(pea.router)
app.include_router(bae.router)
app.include_router(pgs.router)
app.include_router(psw.router)
app.include_router(reservation.router)
app.include_router(equipement.router)
app.include_router(salle.router)

#Autorisation
app.add_middleware(
        CORSMiddleware,
        allow_origins = ["http://localhost:3000"],
        allow_credentials = True,
        allow_methods = ["GET", "POST", "PUT", "DELETE"],
        allow_headers = ["*"],
)

#Message de bienvenue
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")