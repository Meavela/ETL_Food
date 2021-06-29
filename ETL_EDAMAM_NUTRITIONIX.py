from source import Source
import bonobo
import time
import requests
from nutriscore import Nutriscore
from decouple import config
from elasticsearch import Elasticsearch

class ETL_EDAMAM_NUTRITIONIX:
    def __init__(self):
        self.listOfFood = self.get_foodname()
        print(self.listOfFood)
        self.listOfNutrients = self.get_nutrients()
        self.elasticsearch = Elasticsearch(
            cloud_id=config('ELASTIC_CLOUD_ID'),
            http_auth=(config('ELASTIC_USERNAME'), config('ELASTIC_PASSWORD')),
        )
    
    ###
    # Récupération de la liste des nutriments
    ###
    def get_nutrients(self):
        # Initialisation de l'appel à l'API
        ID = config('NUTRITIONAPI_SECRET_ID')
        KEY = config('NUTRITIONAPI_SECRET_KEY')
        headers = {"x-app-id":ID, "x-app-key": KEY, "x-remote-user-id": "0"}
        URL = 'https://trackapi.nutritionix.com/v2/utils/nutrients'
        req = requests.get(URL, headers=headers)
        
        ## Vérification que le code est bien 200
        if req.status_code == 200:
            return req.json()

    ###
    # Récupération d'une liste de noms de nourriture
    ###
    def get_foodname(self):
        # Initialisation de l'appel à l'API
        ID = config('FOODNAMEAPI_SECRET_ID')
        KEY = config('FOODNAMEAPI_SECRET_KEY')
        
        ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        foodname = []
        for i in range(len(ALPHABET)):
            URL = f"https://api.edamam.com/auto-complete?app_id={ID}&app_key={KEY}&q={ALPHABET[i]}"
            req = requests.get(URL)
            
            ## Vérification que le code est bien 200
            if req.status_code == 200:
                foodname = foodname+req.json()
        
        return list(dict.fromkeys(foodname))

    ###
    # Ne prend pas d'input
    # Est lancée une fois au début
    # Permet d'extraire des données
    # Ce sont les données sur lesquelles on va appliquer des transformations
    ###
    def extract_data(self):
        ID = config('NUTRITIONAPI_SECRET_ID')
        KEY = config('NUTRITIONAPI_SECRET_KEY')
        headers = {"x-app-id":ID, "x-app-key": KEY, "x-remote-user-id": "0"}
        # for i in range(len(self.listOfFood)):
        for i in range(1):
            URL = f'https://trackapi.nutritionix.com/v2/search/instant?query={self.listOfFood[i]}&branded=true&common=false&detailed=true&claims=true'
            req = requests.get(URL, headers=headers)

            ## Vérification que le code est bien 200
            if req.status_code == 200:
                json = req.json()
                brandes = json["branded"]
                # Itération sur chaque marque de produit
                for j in range(len(brandes)):
                    yield brandes[j]

    ###
    # Est lancée pour chaque ligne de données
    # Contient toutes les règles de transformation à appliquer sur les données
    ###
    def transform(self,*args):
        # Itération sur chaque nutriment pour récupérer les labels correspondant
        args[0]["new_nutrients"] = []
        for k in range(len(args[0]["full_nutrients"])):
            for nutri in range(len(self.listOfNutrients)):
                if args[0]["full_nutrients"][k]["attr_id"] == self.listOfNutrients[nutri]["attr_id"]:
                    args[0]["new_nutrients"].append({'label':self.listOfNutrients[nutri]["usda_nutr_desc"],'value':args[0]["full_nutrients"][k]['value']})
        del args[0]["full_nutrients"]

        # Récupération du nutriscore du produit
        nutriscore = Nutriscore(args[0]["new_nutrients"])
        args[0]["nutriscore"] = nutriscore.nutriscore

        # Récupération de la photo
        args[0]['photo'] = args[0]['photo']['thumb']

        # Récupération des ingrédients
        args[0]['ingredients'] = []
        ID_RECIPE = config('RECIPEAPI_SECRET_ID')
        KEY_RECIPE = config('RECIPEAPI_SECRET_KEY')
        ID_FOODNAME = config('FOODNAMEAPI_SECRET_ID')
        KEY_FOODNAME = config('FOODNAMEAPI_SECRET_KEY')
        
        ## Appel de l'API des recettes
        URL = f"https://api.edamam.com/api/recipes/v2?app_id={ID_RECIPE}&app_key={KEY_RECIPE}&type=public&q={args[0]['food_name']}"
        req = requests.get(URL)
        
        ## Vérification que le code est bien 200
        if req.status_code == 200:
            jsonrecipe = req.json()
            
            ## Vérification qu'il y a bien quelque chose qui existe
            if jsonrecipe["hits"]:
                ## Récupération des ingrédients
                ingredients = jsonrecipe["hits"][0]["recipe"]["ingredients"]
               
                ## Pour chaque ingrédient
                for i in range(len(ingredients)):
                    ## Récupération de l'id de l'ingrédient
                    foodId = ingredients[i]["foodId"]
                   
                    # Appel de l'API de la nourriture à partir de l'id de l'ingrédient
                    URL = f"https://api.edamam.com/api/food-database/v2/parser?app_id={ID_FOODNAME}&app_key={KEY_FOODNAME}&ingr={foodId}"
                    req = requests.get(URL)
                    
                    ## Vérification que le code est bien 200
                    if req.status_code == 200:
                        jsonfooddb = req.json()
                        
                        ## Récupération du nom de l'ingrédient
                        nameIngr = jsonfooddb["hints"][0]["food"]["label"]
                        args[0]['ingredients'].append(nameIngr)
        
        # Ajout de la source
        args[0]["source_api"] = Source.EDAMAM_NUTRITIONIX.name

        # Récupération de "FR" / "US" ...etc
        args[0]['locale'] = args[0]['locale'].split("_")[1]

        # Suppression des données inutiles
        del args[0]["nix_brand_id"]
        del args[0]["nix_item_id"]
        del args[0]["brand_type"]
        del args[0]["region"]
        del args[0]["brand_name_item_name"]
        del args[0]["serving_qty"]
        del args[0]["serving_weight_grams"]
        del args[0]["serving_unit"]
        del args[0]["nf_calories"]
        del args[0]["new_nutrients"]

        yield args

    ###
    # Est lancée pour chaque ligne de données
    # Ne retourne absolument rien
    ###
    def load(self,*args):
        print(f"----- {args[0]['food_name']} -----")    
        # Check si ça existe en BDD
        body = {"query": {
                    "terms" : { 
                        "product" : [args[0]['food_name']]
                        }
                    }
                }
        result = self.elasticsearch.search(index="products", body=body)
        
        # Si non, insert en BDD
        # print(result["hits"]["hits"])
        if not result["hits"]["hits"]:
            product = {
                "from": args[0]['locale'],
                "source": args[0]['source_api'],
                "product": args[0]['food_name'],
                "brand": args[0]['brand_name'],
                "categories": args[0]['claims'],
                "image": args[0]['photo'],
                "ingredients": args[0]['ingredients'],
                "nutriscore": args[0]['nutriscore']
            }
            print(product)
            self.elasticsearch.index(index="products", body=product)
        time.sleep(5)
    
    ###
    # Permet de configurer le graphique Bonobo
    # Cette configuration est totalement personnalisable
    ###
    def get_graph(self,**options):
        """
        This function builds the graph that needs to be executed.

        :return: bonobo.Graph

        """
        graph = bonobo.Graph()
        graph.add_chain(self.extract_data, self.transform, self.load)

        return graph

    ###
    # Permet de se connecter à des services externes
    ###
    def get_services(self,**options):
        """
        This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
        for runtime injection.

        It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
        let the framework define them. You can also define your own services and naming is up to you.

        :return: dict
        """
        return {}

###
# The __main__ block actually execute the graph.
###
if __name__ == '__main__':
    etl = ETL_EDAMAM_NUTRITIONIX()
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            etl.get_graph(**options),
            services=etl.get_services(**options)
        )