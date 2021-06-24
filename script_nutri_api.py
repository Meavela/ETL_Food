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
            for j in range(len(brandes)):
                brandes[j]["new_nutrients"] = []
                for k in range(len(brandes[j]["full_nutrients"])):
                    for nutri in range(len(listOfNutrients)):
                        if brandes[j]["full_nutrients"][k]["attr_id"] == listOfNutrients[nutri]["attr_id"]:
                            brandes[j]["new_nutrients"].append({'label':listOfNutrients[nutri]["usda_nutr_desc"],'value':brandes[j]["full_nutrients"][k]['value']})
                del brandes[j]["full_nutrients"]
                print(brandes[j])

def calculate_nutriscore():
    score = 0
    badPoints = 0
    goodPoints = 0

    # Bad points
    ## Energie
    ### 0 : <=335
    ### 1 : >335
    ### 2 : >670
    ### 3 : >1005
    ### 4 : >1340
    ### 5 : >1675
    ### 6 : >2010
    ### 7 : >2345
    ### 8 : >2680
    ### 9 : >3015
    ### 10 : >3350
    ## Sucre
    ### 0 : <=4.5
    ### 1 : >4.5
    ### 2 : >9
    ### 3 : >13.5
    ### 4 : >18
    ### 5 : >22.5
    ### 6 : >27
    ### 7 : >31
    ### 8 : >36
    ### 9 : >40
    ### 10 : >45
    ## Acide gras saturés
    ### 0 : <=1
    ### 1 : >1
    ### 2 : >2
    ### 3 : >3
    ### 4 : >4
    ### 5 : >5
    ### 6 : >6
    ### 7 : >7
    ### 8 : >8
    ### 9 : >9
    ### 10 : >10
    ## Sodium
    ### 0 : <=90
    ### 1 : >90
    ### 2 : >180
    ### 3 : >270
    ### 4 : >360
    ### 5 : >450
    ### 6 : >540
    ### 7 : >630
    ### 8 : >720
    ### 9 : >810
    ### 10 : >900

    # Good points
    ## Fruits
    ## Fibres
    ### 0 : <=0.9
    ### 1 : >0.9
    ### 2 : >1.9
    ### 3 : >2.8
    ### 4 : >3.7
    ### 5 : >4.7
    ## Protéines
    ### 0 : <=1.6
    ### 1 : >1.6
    ### 2 : >3.2
    ### 3 : >4.8
    ### 4 : >6.4
    ### 5 : >8.0

    if score <= 0 :
        return "A"
    elif score >= 1 and score <= 10 :
        return "B"
    elif score >= 11 and score <= 20 :
        return "C"
    elif score >= 21 and score <= 30 :
        return "D"
    elif score >= 31 and score <= 40 :
        return "E"


print("----- listOfFood ------")
listOfFood = get_foodname()
print(listOfFood)

print("----- listOfNutrients ------")
listOfNutrients = get_nutrients()
print(listOfNutrients)

print("----- listOfNutriscore ------")
get_nutriscore(listOfFood, listOfNutrients)

