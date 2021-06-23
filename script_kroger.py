import requests

USER = 'etlfood-60a743ceeca67988b7374cbf03085e344520851576200229981'
PASSWORD = 'YKdJEnFXFDdiAL1blQPpbHEpp1XzdXX1Q8tJVB8A'

headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic ZXRsZm9vZC02MGE3NDNjZWVjYTY3OTg4YjczNzRjYmYwMzA4NWUzNDQ1MjA4NTE1NzYyMDAyMjk5ODE6WUtkSkVuRlhGRGRpQUwxYmxRUHBiSEVwcDFYemRYWDFROHRKVkI4QQ=="}
payload = {'grant_type': 'client_credentials','scope': 'product.compact'}

response = requests.post('https://api.kroger.com/v1/connect/oauth2/token', data=payload, headers=headers).json()

print(response)
token = response['access_token']

headers = {'Accept':'application/json', 'Authorization':'Bearer '+token}

data = requests.get('https://api.kroger.com/v1/products?filter.term=food', headers=headers).json()

print(data)
