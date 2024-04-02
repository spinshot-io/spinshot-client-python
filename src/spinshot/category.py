from spinshot.model import Model
from spinshot.resource import Resource
from spinshot.restapiclient import RestAPIClient


class Category(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uid = kwargs.get('uid', '')
        self.title = kwargs.get('title', '')
        self.meta = kwargs.get('meta', {})

    def __str__(self):
        return (f'Category(\n'
                f'  uid:   {self.uid}\n'
                f'  title: {self.title}\n'
                f'  meta:  {self.meta}\n'
                ')')

    def create_json(self):
        return dict(
            title=self.title,
            meta=self.meta
        )

    def update_json(self):
        return dict(
            title=self.title,
            meta=self.meta
        )


class CategoryResource(Resource):
    def __init__(self, client: RestAPIClient):
        super().__init__(client)
        self.endpoint = 'category'
        self.model = Category
