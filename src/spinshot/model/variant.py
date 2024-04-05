from spinshot.model.base import Model


class Variant(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description = kwargs.get('description', '')
        self.sku = kwargs.get('sku', '')
        self.meta = kwargs.get('meta', {})
        self.product = kwargs.get('product', '')

    def __str__(self):
        return (f'Variant(\n'
                f'  uid:         {self.uid}\n'
                f'  description: {self.description}\n'
                f'  sku:         {self.sku}\n'
                f'  product:     {self.product}\n'
                ')')

    def to_dict(self):
        return dict(
            uid=self.uid,
            description=self.description,
            sku=self.sku,
            product=self.product,
            meta=self.meta
        )

