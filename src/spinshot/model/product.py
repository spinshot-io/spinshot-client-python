from spinshot.model.base import Model


class Product(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', '')
        self.sku = kwargs.get('sku', '')
        self.meta = kwargs.get('meta', {})
        self.category = kwargs.get('category', '')

    def __str__(self):
        return (f'Product(\n'
                f'  uid:       {self.uid}\n'
                f'  title:     {self.title}\n'
                f'  sku:       {self.sku}\n'
                f'  category:  {self.category}\n'
                ')')

    def to_dict(self):
        return dict(
            uid=self.uid,
            title=self.title,
            sku=self.sku,
            meta=self.meta,
            category=self.category
        )
