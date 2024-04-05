from spinshot.model.base import Model


class Image(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_filename = kwargs.get('original_filename', '')
        self.image = kwargs.get('image', '')
        self.meta = kwargs.get('meta', {})

        self.product = kwargs.get('product')
        self.variant = kwargs.get('variant')

        self._file = None

    def __str__(self):
        return (f'Image(\n'
                f'  uid:                {self.uid}\n'
                f'  product:            {self.product}\n'
                f'  variant:            {self.variant}\n'
                f'  original_filename:  {self.original_filename}\n'
                f'  meta:               {self.meta}\n'
                ')')

    def set_image(self, original_filename: str, fh):
        self._file = (original_filename, fh)

    def to_dict(self):
        data = dict(
            uid=self.uid,
            product=self.product,
            variant=self.variant,
            meta=self.meta
        )

        if self._file is not None:
            data['files'] = {'image': self._file}

        return data
