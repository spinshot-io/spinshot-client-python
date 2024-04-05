from spinshot.model.base import Model
from spinshot.restapiclient import RestAPIClient


class Resource:

    def __init__(self, client: RestAPIClient):
        self.client = client
        self.model = None
        self.endpoint = None

    def list(self, **kwargs) -> list:
        params = {}
        for k, v in kwargs.items():
            if isinstance(v, Model):
                params[k] = v.uid
            else:
                params[k] = v

        response = self.client.list(self.endpoint, params)
        results = []
        for result in response['results']:
            results.append(self.model(**result))
        return results

    def retrieve(self, pk: str):
        response = self.client.retrieve(self.endpoint, pk)
        instance = self.model(**response)
        return instance

    def create(self, instance):
        response = self.client.create(self.endpoint, instance)
        instance = self.model(**response)
        return instance

    def update(self, instance):
        response = self.client.update(self.endpoint, instance)
        instance = self.model(**response)
        return instance

    def delete(self, instance) -> bool:
        self.client.delete(self.endpoint, instance)
        return True
