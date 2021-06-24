import bonobo
import requests
import csv

FABLABS_API_URL = 'https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=cereals&json=true'

class Product:
    def __init__(self, name, nova, nutriscore) -> None:
        self.name = name
        self.nova = nova
        self.nutriscore = nutriscore

def extract_fablabs():
    requete = requests.get(FABLABS_API_URL).json().get('products')
    data = []
    for i in range(24):
        product = Product(requete[i].get('product_name'), requete[i].get('nova_group'), requete[i].get('nutriscore_grade'))
        data.append(product)

    return data

def load(args):
    """for product in args:
        print(f"{product.name} nova:{product.nova} nutriscore:{product.nutriscore}")"""
    i = 0
    for row in args:
        if i < 1:
            print(row)
        i += 1
    

def loadCsv():
    file = open("en.openfoodfacts.org.products.csv")
    reader = csv.reader(file, delimiter="\t")
    return reader

def get_graph(**options):
    """
    This function builds the graph that needs to be executed.

    :return: bonobo.Graph

    """
    graph = bonobo.Graph()
    graph.add_chain(bonobo.CsvReader('en.openfoodfacts.org.products.csv', delimiter="\t"), bonobo.Limit(10), bonobo.PrettyPrinter())

    return graph


def get_services(**options):
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
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options),
            services=get_services(**options)
        )