from spinshot.model.variant import Variant
from spinshot.resource.base import Resource
from spinshot.restapiclient import RestAPIClient


class VariantResource(Resource):
    def __init__(self, client: RestAPIClient):
        super().__init__(client)
        self.endpoint = 'variant'
        self.model = Variant
