from spinshot.model import Model
from spinshot.product import Product
from spinshot.resource import Resource
from spinshot.restapiclient import RestAPIClient
from spinshot.variant import Variant


class Image(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_filename = kwargs.get('original_filename', '')
        self.image = kwargs.get('image', '')
        self.meta = kwargs.get('meta', {})

        self.product = kwargs.get('product', '')
        self.variant = kwargs.get('variant', '')

        self._file = None

    def __setattr__(self, key, value):
        if key == 'product':
            self.set_product(value)
        elif key == 'variant':
            self.set_variant(value)
        else:
            super().__setattr__(key, value)

    def __str__(self):
        return (f'Image(\n'
                f'  uid:                {self.uid}\n'
                f'  product:            {self.product}\n'
                f'  variant:            {self.variant}\n'
                f'  original_filename:  {self.original_filename}\n'
                f'  meta:               {self.meta}\n'
                ')')

    def set_product(self, product):
        if isinstance(product, Product):
            self.__dict__['product'] = product.uid
        else:
            self.__dict__['product'] = product

    def set_variant(self, variant):
        if isinstance(variant, Variant):
            self.__dict__['variant'] = variant.uid
        else:
            self.__dict__['variant'] = variant

    def set_image(self, original_filename: str, fh):
        self._file = (original_filename, fh)

    def create_json(self):
        data = dict(
            product=self.product,
            variant=self.variant,
            meta=self.meta
        )

        if self._file is not None:
            data['files'] = {'image': self._file}

        return data

    def update_json(self):
        data = dict(
            meta=self.meta
        )

        if self._file is not None:
            data['files'] = {'image': self._file}

        return data


class ImageResource(Resource):
    def __init__(self, client: RestAPIClient):
        super().__init__(client)
        self.endpoint = 'image'
        self.model = Image
