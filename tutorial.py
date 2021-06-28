import bonobo
import json
from Product import Product
from source import Source
from bonobo.config import use_raw_input
from decouple import config
from elasticsearch import Elasticsearch
from getNutriscore import calculeNutriscore

class openETL:
    def __init__(self):
        self.elasticsearch = Elasticsearch(
            cloud_id=config('ELASTIC_CLOUD_ID'),
            http_auth=(config('ELASTIC_USERNAME'), config('ELASTIC_PASSWORD')),
        )
        self.elasticsearch.delete_by_query(index="products", body={"query": {"match_all": {}}})

    @use_raw_input
    def load(self, product):
        if (product.nutriscore_grade == ""):
            myProduct = Product(product.product_name, calculeNutriscore(product), product.brands, product.categories, product.ingredients_text, product.origins, product.image_url)
        else:
            myProduct = Product(product.product_name, product.nutriscore_grade, product.brands, product.categories, product.ingredients_text, product.origins, product.image_url)
        print(json.dumps(myProduct.__dict__))
    
        # Check si ça existe en BDD
        result = self.elasticsearch.search(index="products", body={"query":{"match": {"product": product.product_name}}})
        # Si non, insert en BDD
        print(result["hits"]["hits"])
        if not result["hits"]["hits"]:
            product = {
                "from": myProduct.origins,
                "source": myProduct.source,
                "product": myProduct.name,
                "brand": myProduct.brands,
                "categories": myProduct.categories,
                "image": myProduct.image,
                "ingredients": myProduct.ingredients,
                "nutriscore": myProduct.nutriscore
            }
            print("*** To insert ***")
            print(product)
            response = self.elasticsearch.index(index="products", body=product)
            print(response['result'])


    def get_graph(self, **options):
        """
        This function builds the graph that needs to be executed.

        :return: bonobo.Graph

        """
        graph = bonobo.Graph()
        graph.add_chain(bonobo.CsvReader('en.openfoodfacts.org.products.csv', delimiter="\t"), bonobo.Limit(3), self.load)

        return graph


    def get_services(self, **options):
        """
        This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
        for runtime injection.

        It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
        let the framework define them. You can also define your own services and naming is up to you.

        :return: dict
        """
        return {}


# The __main__ block actually execute the graph.
if __name__ == '__main__':
    etl = openETL()
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            etl.get_graph(**options),
            services=etl.get_services(**options)
        )