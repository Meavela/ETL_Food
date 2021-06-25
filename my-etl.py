import bonobo
import requests
from nutriscore import Nutriscore
from decouple import config

class ETL:
    def __init__(self):
        self.listOfFood = self.get_foodname()
        self.listOfNutrients = self.get_nutrients()
    
    def get_nutrients(self):
        ID = config('NUTRITIONAPI_SECRET_ID')
        KEY = config('NUTRITIONAPI_SECRET_KEY')
        headers = {"x-app-id":ID, "x-app-key": KEY, "x-remote-user-id": "0"}
        URL = 'https://trackapi.nutritionix.com/v2/utils/nutrients'
        req = requests.get(URL, headers=headers)
        if req.status_code == 200:
            print(req.json())
            return req.json()

    def get_foodname(self):
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
            print(URL)
            req = requests.get(URL, headers=headers)
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
        """Placeholder, change, rename, remove... """
        # print("------------")    
        args[0]["new_nutrients"] = []
        # Itération sur chaque nutriment pour récupérer les labels correspondant
        for k in range(len(args[0]["full_nutrients"])):
            for nutri in range(len(self.listOfNutrients)):
                if args[0]["full_nutrients"][k]["attr_id"] == self.listOfNutrients[nutri]["attr_id"]:
                    args[0]["new_nutrients"].append({'label':self.listOfNutrients[nutri]["usda_nutr_desc"],'value':args[0]["full_nutrients"][k]['value']})
        del args[0]["full_nutrients"]

        # Récupération du nutriscore du produit
        nutriscore = Nutriscore(args[0]["new_nutrients"])
        args[0]["nutriscore"] = nutriscore.nutriscore

        args[0]['photo'] = args[0]['photo']['thumb']

        del args[0]["nix_brand_id"]
        del args[0]["nix_item_id"]
        del args[0]["brand_type"]
        del args[0]["region"]
        del args[0]["locale"]
        del args[0]["brand_name_item_name"]
        del args[0]["serving_qty"]
        del args[0]["new_nutrients"]

        yield args

    ###
    # Est lancée pour chaque ligne de données
    # Ne retourne absolument rien
    ###
    def load(self,*args):
        """Placeholder, change, rename, remove... """
        print(*args)

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
    etl = ETL()
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            etl.get_graph(**options),
            services=etl.get_services(**options)
        )