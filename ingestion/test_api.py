import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

client_id = os.getenv("FT_CLIENT_ID")
client_secret = os.getenv("FT_CLIENT_SECRET")

print("Client ID trouvé :", client_id is not None)
print("Secret trouvé :", client_secret is not None)


reponse_token = requests.post(
    "https://entreprise.francetravail.fr/connexion/oauth2/access_token",
    params={"realm": "/partenaire"},
    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api_offresdemploiv2 o2dsoffre",
    },
)

print("Statut :", reponse_token.status_code)

token = reponse_token.json()["access_token"]


reponse_offres = requests.get(
    "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search",
    headers={"Authorization": f"Bearer {token}"},
    params={"range": "0-4"},
)

print("Statut offres :", reponse_offres.status_code)

offres = reponse_offres.json()["resultats"]

with open("data/exemple_offres.json", "w", encoding="utf-8") as fichier:
    json.dump(offres, fichier, indent=2, ensure_ascii=False)

print("Nombre d'offres enregistrées :", len(offres))