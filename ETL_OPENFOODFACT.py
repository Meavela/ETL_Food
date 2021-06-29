import bonobo
from Product import Product
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
        #self.elasticsearch.delete_by_query(index="products", body={"query": {"match_all": {}}})

    def load(self, product):
        # Check si ça existe en BDD
        result = self.elasticsearch.search(index="products", body={"query":{"terms": {"product": [product.name]}}})
        # Si non, insert en BDD
        if not result["hits"]["hits"]:
            product = {
                "from": product.origins,
                "source": product.source,
                "product": product.name,
                "brand": product.brands,
                "categories": product.categories,
                "image": product.image,
                "ingredients": product.ingredients,
                "nutriscore": product.nutriscore
            }
            response = self.elasticsearch.index(index="products", body=product)
        else:
            for productBD in result["hits"]["hits"]:
                if (productBD["_source"]["from"] == "" and product.origins != ""):
                    self.elasticsearch.update(index="products", doc_type="_doc", id=productBD["_id"], body={"doc": {"from":product.origins}})
                if (productBD["_source"]["brand"] == "" and product.brands != ""):
                    self.elasticsearch.update(index="products", doc_type="_doc", id=productBD["_id"], body={"doc": {"brand":product.brands}})
                if (productBD["_source"]["categories"] == "" and product.categories != ""):
                    self.elasticsearch.update(index="products", doc_type="_doc", id=productBD["_id"], body={"doc": {"categories":product.categories}})
                if (productBD["_source"]["image"] == "" and product.image != ""):
                    self.elasticsearch.update(index="products", doc_type="_doc", id=productBD["_id"], body={"doc": {"image":product.image}})
                if (productBD["_source"]["ingredients"] == "" and product.ingredients != ""):
                    self.elasticsearch.update(index="products", doc_type="_doc", id=productBD["_id"], body={"doc": {"ingredients":product.ingredients}})
                if (productBD["_source"]["categories"] == "" and product.categories != ""):
                    self.elasticsearch.update(index="products", doc_type="_doc", id=productBD["_id"], body={"doc": {"categories":product.categories}})
                if (productBD["_source"]["nutriscore"].islower()):
                    self.elasticsearch.update(index="products", doc_type="_doc", id=productBD["_id"], body={"doc": {"nutriscore":product.nutriscore}})

    @use_raw_input
    def transform(self, product):
        if (product.nutriscore_grade == ""):
            myProduct = Product(product.product_name, calculeNutriscore(product), product.brands, product.categories, product.ingredients_text, product.countries_en, product.image_url)
        else:
            myProduct = Product(product.product_name, product.nutriscore_grade.upper(), product.brands, product.categories, product.ingredients_text, product.countries_en, product.image_url)
        yield myProduct


    def get_graph(self, **options):
        """
        This function builds the graph that needs to be executed.

        :return: bonobo.Graph

        """
        graph = bonobo.Graph()
        graph.add_chain(bonobo.CsvReader('en.openfoodfacts.org.products.csv', delimiter="\t"), self.transform, self.load)

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