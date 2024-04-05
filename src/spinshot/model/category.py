from spinshot.model.base import Model


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

    def to_dict(self):
        return dict(
            uid=self.uid,
            title=self.title,
            meta=self.meta
        )
