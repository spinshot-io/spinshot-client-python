# Spinshot Python Client API

## Installation 

    python -m venv venv
    source venv bin activate
    pip  install -e .

## Configuration

Create a configuration file

`/etc/spinshot/config` or `~/.spinshot/config`

    [default]
    HOST = api.spinshot.io
    PORT = 443
    USE_SSL = yes
    SECRET_KEY = 

## Using the spinshot cli

    spinshot [-c configfile] [-e environment] <resource> <action> [parameters]

resource can be one of

- category
- product
- variant
- image

action can be one of 

- list
- create
- retrieve
- update
- delete

each resource/action combination has its one set of parameters which can be displayed using

    spinshot <resource> <action> -h

## Examples:

    client = SpinshotClient()
    
    for product in client.products.list():
        print(product)
        
        for variant in client.variants.list(product=product):
            print(variant)

        for image in client.images.list(product=product):
            print(image)

