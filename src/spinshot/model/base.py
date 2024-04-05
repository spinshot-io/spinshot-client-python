import json


class Model:
    def __init__(self, **kwargs):
        self.uid = kwargs.get('uid', None)

    def __setattr__(self, name, value):
        # make sure meta is a dict
        if name == 'meta':
            if isinstance(value, str):
                value = json.loads(value)

        super().__setattr__(name, value)
