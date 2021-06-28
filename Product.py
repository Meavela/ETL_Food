from source import Source

class Product:
    def __init__(self, name, nutriscore, brands, categories, ingredients, origins, image) -> None:
        self.name = name
        self.nutriscore = nutriscore
        self.brands = brands
        self.categories = categories
        self.ingredients = ingredients
        self.origins = origins
        self.image = image
        self.source = Source.OPENFOODFACT.name