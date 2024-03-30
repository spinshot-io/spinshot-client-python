from spinshot.category import CategoryResource
from spinshot.image import ImageResource
from spinshot.product import ProductResource
from spinshot.restapiclient import RestAPIClient
from spinshot.variant import VariantResource


class SpinshotClient:
    def __init__(self, secret_key=None, host=None, port=None, use_ssl=None):
        api_client = RestAPIClient(secret_key, host, port, use_ssl)
        self.categories = CategoryResource(api_client)
        self.products = ProductResource(api_client)
        self.variants = VariantResource(api_client)
        self.images = ImageResource(api_client)
