from spinshot.model.base import Model


class Variant(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.sku = kwargs.get('sku', '')
        self.meta = kwargs.get('meta', {})
        self.product = kwargs.get('product', '')

    def __str__(self):
        return (f'Variant(\n'
                f'  uid:         {self.uid}\n'
                f'  name:        {self.name}\n'
                f'  sku:         {self.sku}\n'
                f'  product:     {self.product}\n'
                ')')

    def to_dict(self):
        return dict(
            uid=self.uid,
            name=self.name,
            sku=self.sku,
            product=self.product,
            meta=self.meta
        )

