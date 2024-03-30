# Spinshot Python Client API


## Configuration

Create a configuration file

`/etc/spinshot/config` or `~/.spinshot/config`

    [default]
    HOST = api.spinshot.io
    PORT = 443
    USE_SSL = yes
    SECRET_KEY = 


## Examples:

    client = SpinshotClient()
    
    for product in client.products.list():
        print(product)
        
        for variant in client.variants.list(product=product):
            print(variant)

        for image in client.images.list(product=product):
            print(image)

