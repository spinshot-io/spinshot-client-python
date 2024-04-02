from spinshot.category import Category
from spinshot.model import Model
from spinshot.restapiclient import RestAPIClient
from spinshot.resource import Resource


class Product(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', '')
        self.sku = kwargs.get('sku', '')
        self.meta = kwargs.get('meta', {})


        category = kwargs.get('category', '')
        if isinstance(category, dict):
            self.category = Category(**category)
        else:
            self.category = category

    def __setattr__(self, key, value):
        if key == 'category':
            self.set_category(value)
        else:
            super().__setattr__(key, value)

    def __str__(self):
        return (f'Product(\n'
                f'  uid:       {self.uid}\n'
                f'  title:     {self.title}\n'
                f'  sku:       {self.sku}\n'
                f'  category:  {self.category}\n'
                ')')

    def set_category(self, category):
        if isinstance(category, Category):
            self.__dict__['category'] = category.uid
        else:
            self.__dict__['category'] = category

    def create_json(self):
        return dict(
            category=self.category,
            title=self.title,
            sku=self.sku,
            meta=self.meta
        )

    def update_json(self):
        return dict(
            title=self.title,
            sku=self.sku,
            meta=self.meta
        )


class ProductResource(Resource):
    def __init__(self, client: RestAPIClient):
        super().__init__(client)
        self.endpoint = 'product'
        self.model = Product
