from nutriscore import Nutriscore
import requests
import random
from decouple import config

def get_foodname():
    ID = config('FOODNAMEAPI_SECRET_ID')
    KEY = config('FOODNAMEAPI_SECRET_KEY')
    ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    foodname = []
    for i in range(len(ALPHABET)):
        URL = f"https://api.edamam.com/auto-complete?app_id={ID}&app_key={KEY}&q={ALPHABET[i]}"
        req = requests.get(URL)
        if req.status_code == 200:
            foodname = foodname+req.json()
    return foodname

def get_nutrients():
    ID = config('NUTRITIONAPI_SECRET_ID')
    KEY = config('NUTRITIONAPI_SECRET_KEY')
    headers = {"x-app-id":ID, "x-app-key": KEY, "x-remote-user-id": "0"}
    URL = 'https://trackapi.nutritionix.com/v2/utils/nutrients'
    req = requests.get(URL, headers=headers)
    if req.status_code == 200:
        print(req.json())
        return req.json()

def get_nutriscore(listOfFood, listOfNutrients):
    ID = config('NUTRITIONAPI_SECRET_ID')
    KEY = config('NUTRITIONAPI_SECRET_KEY')
    headers = {"x-app-id":ID, "x-app-key": KEY, "x-remote-user-id": "0"}
    # for i in range(len(listOfFood)):
    for i in range(1):
        URL = f'https://trackapi.nutritionix.com/v2/search/instant?query={listOfFood[i]}&branded=true&common=false&detailed=true'
        print(URL)
        req = requests.get(URL, headers=headers)
        if req.status_code == 200:
            json = req.json()
            brandes = json["branded"]
            # itération sur chaque marque de produit
            for j in range(len(brandes)):
                brandes[j]["new_nutrients"] = []
                # Itération sur chaque nutriment pour récupérer les labels correspondant
                for k in range(len(brandes[j]["full_nutrients"])):
                    for nutri in range(len(listOfNutrients)):
                        if brandes[j]["full_nutrients"][k]["attr_id"] == listOfNutrients[nutri]["attr_id"]:
                            brandes[j]["new_nutrients"].append({'label':listOfNutrients[nutri]["usda_nutr_desc"],'value':brandes[j]["full_nutrients"][k]['value']})
                del brandes[j]["full_nutrients"]

                # Récupération du nutriscore du produit
                nutriscore = Nutriscore(brandes[j]["new_nutrients"])
                brandes[j]["nutriscore"] = nutriscore.nutriscore

                print(brandes[j])



print("----- listOfFood ------")
listOfFood = get_foodname()
print(listOfFood)

print("----- listOfNutrients ------")
listOfNutrients = get_nutrients()
print(listOfNutrients)

print("----- listOfNutriscore ------")
get_nutriscore(listOfFood, listOfNutrients)

