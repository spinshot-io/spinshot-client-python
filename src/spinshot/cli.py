import argparse
import glob
import os
from argparse import ArgumentTypeError

from spinshot.resource.category import Category
from spinshot.client import SpinshotClient
from spinshot.resource.image import Image
from spinshot.resource.product import Product
from spinshot.restapiclient import RestApiException
from spinshot.resource.variant import Variant


def main_cli():
    # Initialize parser
    parser = argparse.ArgumentParser(
        description='spinshot command line interface'
    )

    parser.add_argument('-v', '--verbose', help='Increase the verbosity')
    parser.add_argument('-c', '--config', help='Config file')
    parser.add_argument('-e', '--environment', help='Config file environment', default='default')

    sub_parsers = parser.add_subparsers(help='resource type', dest='resource', required=True)

    create_category_sub_parsers(sub_parsers)
    create_product_sub_parsers(sub_parsers)
    create_variant_sub_parsers(sub_parsers)
    create_image_sub_parsers(sub_parsers)

    args = parser.parse_args()

    handlers = dict(
        category=dict(
            list=category_list,
            create=category_create,
            retrieve=category_retrieve,
            update=category_update,
            delete=category_delete,
        ),
        product=dict(
            list=product_list,
            create=product_create,
            retrieve=product_retrieve,
            update=product_update,
            delete=product_delete,
        ),
        variant=dict(
            list=variant_list,
            create=variant_create,
            retrieve=variant_retrieve,
            update=variant_update,
            delete=variant_delete,
        ),
        image=dict(
            list=image_list,
            create=image_create,
            retrieve=image_retrieve,
            update=image_update,
            delete=image_delete,
        ),
    )

    try:
        client = SpinshotClient(args)
        handlers[args.resource][args.command](client, args)
    except RestApiException as e:
        print(f"An error occured: {e}")


def create_category_sub_parsers(sub_parsers):
    parser = sub_parsers.add_parser('category', help='categories')
    sub_parsers, list, create, retrieve, update, delete = create_default_sub_parsers(parser)

    create.add_argument('-t', '--title', help='category title', required=True)

    update.add_argument('-t', '--title', help='category title', required=False)


def create_product_sub_parsers(sub_parsers):
    parser = sub_parsers.add_parser('product', help='products')
    sub_parsers, list, create, retrieve, update, delete = create_default_sub_parsers(parser)

    list.add_argument('-C', '--category', help='filter by category uid')

    create.add_argument('-t', '--title', help='product title', required=True)
    create.add_argument('-s', '--sku', help='product sku', default='')
    create.add_argument('-C', '--category', help='category uid')

    update.add_argument('-t', '--title', help='product title')
    update.add_argument('-s', '--sku', help='product sku', default='')
    update.add_argument('-C', '--category', help='category uid')


def create_variant_sub_parsers(sub_parsers):
    parser = sub_parsers.add_parser('variant', help='variants')
    sub_parsers, list, create, retrieve, update, delete = create_default_sub_parsers(parser)

    list.add_argument('-P', '--product', help='filter by product uid')

    create.add_argument('-P', '--product', help='product uid', required=True)
    create.add_argument('-n', '--name', help='variant name', required=True)
    create.add_argument('-s', '--sku', help='variant sku', default='')

    update.add_argument('-d', '--description', help='variant description')
    update.add_argument('-s', '--sku', help='variant sku', default='')


def create_image_sub_parsers(sub_parsers):
    parser = sub_parsers.add_parser('image', help='images')
    sub_parsers, list, create, retrieve, update, delete = create_default_sub_parsers(parser)

    list.add_argument('-P', '--product', help='filter by product uid')
    list.add_argument('-V', '--variant', help='filter by variant uid')

    group = create.add_mutually_exclusive_group(required=True)
    group.add_argument('-P', '--product', help='product uid')
    group.add_argument('-V', '--variant', help='variant uid')

    group = create.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='file name')
    group.add_argument('-p', '--pattern', help='file pattern')

    update.add_argument('-f', '--file', help='file name')


def create_default_sub_parsers(parser):
    sub_parsers = parser.add_subparsers(help='command', dest='command', required=True)

    list_parser = sub_parsers.add_parser('list', help='list resource')
    list_parser.add_argument('-q', '--query', help='search for text on the resource')

    create_parser = sub_parsers.add_parser('create', help='create resource')
    create_parser.add_argument('-m', '--meta', help='resource meta data', default='{}')

    retrieve_parser = sub_parsers.add_parser('retrieve', help='retrieve resource')
    retrieve_parser.add_argument('-u', '--uid', help='resource uid', required=True)

    update_parser = sub_parsers.add_parser('update', help='update resource')
    update_parser.add_argument('-u', '--uid', help='resource uid', required=True)
    update_parser.add_argument('-m', '--meta', help='resource meta data', default='{}')

    delete_parser = sub_parsers.add_parser('delete', help='delete resource')
    delete_parser.add_argument('-u', '--uid', help='resource uid', required=True)

    return sub_parsers, list_parser, create_parser, retrieve_parser, update_parser, delete_parser


def category_list(client, args):
    results = client.categories.list()
    for result in results:
        print(result)


def category_create(client, args):
    category = Category(title=args.title)

    if args.meta:
        category.meta = args.meta

    category = client.categories.create(category)
    print(category)


def category_retrieve(client, args):
    category = client.categories.retrieve(args.uid)
    print(category)


def category_update(client, args):
    category = client.categories.retrieve(args.uid)

    if args.title:
        category.title = args.title

    if args.meta:
        category.meta = args.meta

    category = client.categories.update(category)
    print(category)


def category_delete(client, args):
    category = client.categories.retrieve(args.uid)
    client.categories.delete(category)
    print("category deleted")


def product_list(client, args):
    results = client.products.list(category=args.category)
    for result in results:
        print(result)


def product_create(client, args):
    product = Product(title=args.title, sku=args.sku, meta=args.meta, category=args.category)
    product = client.products.create(product)
    print(product)


def product_retrieve(client, args):
    product = client.products.retrieve(args.uid)
    print(product)


def product_update(client, args):
    product = client.products.retrieve(args.uid)
    if args.title:
        product.title = args.title

    if args.sku:
        product.sku = args.sku

    if args.meta:
        product.meta = args.meta

    if args.category:
        product.category = args.category

    product = client.products.update(product)
    print(product)


def product_delete(client, args):
    product = client.products.retrieve(args.uid)
    client.products.delete(product)
    print("product deleted")


def variant_list(client, args):
    results = client.variants.list(product=args.product)
    for result in results:
        print(result)


def variant_create(client, args):
    variant = Variant(product=args.product, name=args.name, sku=args.sku, meta=args.meta)
    variant = client.variants.create(variant)
    print(variant)


def variant_retrieve(client, args):
    variant = client.variants.retrieve(args.uid)
    print(variant)


def variant_update(client, args):
    variant = client.variants.retrieve(args.uid)

    if args.name:
        variant.name = args.name

    if args.sku:
        variant.sku = args.sku

    if args.meta:
        variant.meta = args.meta

    variant = client.variants.update(variant)
    print(variant)


def variant_delete(client, args):
    variant = client.variants.retrieve(args.uid)
    client.variants.delete(variant)
    print("variant deleted")


def image_list(client, args):
    results = client.images.list(product=args.product, variant=args.variant)
    for result in results:
        print(result)


def image_create(client, args):
    if args.file:
        if not os.path.exists(args.file):
            raise ArgumentTypeError("File does not exist")
        if not os.path.isfile(args.file):
            raise ArgumentTypeError("File is not a file")

        _image_create(args, args.file)

    if args.pattern:
        home = os.path.expanduser("~")
        pattern = args.pattern.replace('~', home)
        for filename in glob.glob(pattern):
            print(filename)
            _image_create(client, args, filename)


def _image_create(client, args, filename):
    image = Image(product=args.product, variant=args.variant, meta=args.meta)
    original_filename = os.path.basename(filename)
    image.set_image(original_filename, open(filename, 'rb'))
    image = client.images.create(image)
    print(image)


def image_retrieve(client, args):
    image = client.images.retrieve(args.uid)
    print(image)


def image_update(client, args):
    image = client.images.retrieve(args.uid)

    if args.meta:
        image.meta = args.meta

    client.images.update(image)
    print(image)


def image_delete(client, args):
    image = client.images.retrieve(args.uid)
    client.images.delete(image)
    print("image deleted")
