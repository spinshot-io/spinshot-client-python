from spinshot.model.image import Image
from spinshot.resource.base import Resource
from spinshot.restapiclient import RestAPIClient


class ImageResource(Resource):
    def __init__(self, client: RestAPIClient):
        super().__init__(client)
        self.endpoint = 'image'
        self.model = Image
