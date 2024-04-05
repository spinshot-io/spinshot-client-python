from spinshot.model.product import Product
from spinshot.resource.base import Resource
from spinshot.restapiclient import RestAPIClient


class ProductResource(Resource):
    def __init__(self, client: RestAPIClient):
        super().__init__(client)
        self.endpoint = 'product'
        self.model = Product
