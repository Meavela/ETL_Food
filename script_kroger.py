import requests
import random
from decouple import config

###
# Fonction d'Initialisation pour l'API Kroger
# Retourne le token sous forme de Header
###
def initilization():
    # Get config from the .env file
    USER = config('SECRET_ID')
    PASSWORD = config('SECRET_MDP')

    # Initialisation des headers et du payload
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic ZXRsZm9vZC02MGE3NDNjZWVjYTY3OTg4YjczNzRjYmYwMzA4NWUzNDQ1MjA4NTE1NzYyMDAyMjk5ODE6WUtkSkVuRlhGRGRpQUwxYmxRUHBiSEVwcDFYemRYWDFROHRKVkI4QQ=="}
    payload = {'grant_type': 'client_credentials','scope': 'product.compact'}

    # Récupération du token
    response = requests.post('https://api.kroger.com/v1/connect/oauth2/token', data=payload, headers=headers).json()
    print(f"Token response : {response}")
    token = response['access_token']

    # Génération du header à partir du token
    headers = {'Accept':'application/json', 'Authorization':'Bearer '+token}

    return headers


def extract_data(turns, headers):
    data = []
    for i in range(0,turns):
        print(f"---- {i} ----")
        # Génération d'un ProductId aléatoire à 13 caractères
        x = round(random.uniform(0, 9.9))**11
        productId = ""
        for j in range(13-len(str(x))):
            productId += "0"
        productId += f"{x}"
        print(f"ProductId : {productId}")

        # Call de l'API en passant le ProductId
        url = f"https://api.kroger.com/v1/products?filter.productId={productId}"
        print(f"Url : {url}")
        req = requests.get(url, headers=headers)

        # Vérification que le call n'a pas renvoyé un code d'erreur
        if req.status_code == 200:
            json = req.json()

            # Vérification que le JSON possède des données (et donc que le ProductId correspond bien à un produit)
            if json["data"]:
                print(json)
                data += req.json()
    
    return data

turns = 100

headers = initilization()
products = extract_data(turns, headers)

print(f"Nombre de produits trouvés : {len(products)} / {turns}")
