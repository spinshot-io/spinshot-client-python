from spinshot.model import Model
from spinshot.product import Product
from spinshot.resource import Resource
from spinshot.restapiclient import RestAPIClient


class Variant(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = kwargs.get('description', '')
        self.sku = kwargs.get('sku', '')
        self.meta = kwargs.get('meta', {})
        self.product = kwargs.get('product', '')

    def __setattr__(self, key, value):
        if key == 'product':
            self.set_product(value)
        else:
            super().__setattr__(key, value)

    def __str__(self):
        return (f'Variant(\n'
                f'  uid:         {self.uid}\n'
                f'  description: {self.description}\n'
                f'  sku:         {self.sku}\n'
                f'  product:     {self.product}\n'
                ')')

    def set_product(self, product):
        if isinstance(product, Product):
            self.__dict__['product'] = product.uid
        else:
            self.__dict__['product'] = product

    def create_json(self):
        return dict(
            description=self.description,
            sku=self.sku,
            product=self.product,
            meta=self.meta
        )

    def update_json(self):
        return dict(
            description=self.description,
            sku=self.sku,
            meta=self.meta
        )


class VariantResource(Resource):
    def __init__(self, client: RestAPIClient):
        super().__init__(client)
        self.endpoint = 'variant'
        self.model = Variant
