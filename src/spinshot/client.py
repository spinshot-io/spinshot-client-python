from spinshot.resource.category import CategoryResource
from spinshot.resource.image import ImageResource
from spinshot.resource.product import ProductResource
from spinshot.restapiclient import RestAPIClient
from spinshot.resource.variant import VariantResource


class SpinshotClient:
    def __init__(self, args):
        api_client = RestAPIClient(args)
        self.categories = CategoryResource(api_client)
        self.products = ProductResource(api_client)
        self.variants = VariantResource(api_client)
        self.images = ImageResource(api_client)
