from spinshot.model.category import Category
from spinshot.resource.base import Resource
from spinshot.restapiclient import RestAPIClient


class CategoryResource(Resource):
    def __init__(self, client: RestAPIClient):
        super().__init__(client)
        self.endpoint = 'category'
        self.model = Category
