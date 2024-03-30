import argparse
import glob
import os
from argparse import ArgumentError, ArgumentTypeError

from spinshot.category import Category
from spinshot.client import SpinshotClient
from spinshot.image import Image
from spinshot.product import Product
from spinshot.restapiclient import RestApiException
from spinshot.variant import Variant

CLIENT = SpinshotClient()


def main_cli():
    # Initialize parser
    parser = argparse.ArgumentParser(
        description='spinshot command line interface'
    )

    parser.add_argument('-v', '--verbose', help='Increase the verbosity')

    sub_parsers = parser.add_subparsers(help='resource type', dest='resource')

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
        handlers[args.resource][args.command](args)
    except RestApiException as e:
        print(f"operation failed: {e}")


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
    create.add_argument('-d', '--description', help='variant description', required=True)
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
    sub_parsers = parser.add_subparsers(help='command', dest='command')

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


def category_list(args):
    results = CLIENT.categories.list()
    for result in results:
        print(result)


def category_create(args):
    category = Category(title=args.title)
    category = CLIENT.categories.create(category)
    print(category)


def category_retrieve(args):
    category = CLIENT.categories.retrieve(args.uid)
    print(category)


def category_update(args):
    category = CLIENT.categories.retrieve(args.uid)
    if args.title:
        category.title = args.title
    category = CLIENT.categories.update(category)
    print(category)


def category_delete(args):
    category = CLIENT.categories.retrieve(args.uid)
    CLIENT.categories.delete(category)
    print("category deleted")


def product_list(args):
    results = CLIENT.products.list(category=args.category)
    for result in results:
        print(result)


def product_create(args):
    product = Product(title=args.title, sku=args.sku, meta=args.meta, category=args.category)
    product = CLIENT.products.create(product)
    print(product)


def product_retrieve(args):
    product = CLIENT.products.retrieve(args.uid)
    print(product)


def product_update(args):
    product = CLIENT.products.retrieve(args.uid)
    if args.title:
        product.title = args.title

    if args.sku:
        product.sku = args.sku

    if args.meta:
        product.meta = args.meta

    if args.category:
        product.category = args.category

    product = CLIENT.products.update(product)
    print(product)


def product_delete(args):
    product = CLIENT.products.retrieve(args.uid)
    CLIENT.products.delete(product)
    print("product deleted")


def variant_list(args):
    results = CLIENT.variants.list(product=args.product)
    for result in results:
        print(result)


def variant_create(args):
    variant = Variant(product=args.product, description=args.description, sku=args.sku, meta=args.meta)
    variant = CLIENT.variants.create(variant)
    print(variant)


def variant_retrieve(args):
    variant = CLIENT.variants.retrieve(args.uid)
    print(variant)


def variant_update(args):
    variant = CLIENT.variants.retrieve(args.uid)

    if args.description:
        variant.description = args.description

    if args.sku:
        variant.sku = args.sku

    if args.meta:
        variant.meta = args.meta

    variant = CLIENT.variants.update(variant)
    print(variant)


def variant_delete(args):
    variant = CLIENT.variants.retrieve(args.uid)
    CLIENT.variants.delete(variant)
    print("variant deleted")


def image_list(args):
    results = CLIENT.images.list(product=args.product, variant=args.variant)
    for result in results:
        print(result)


def image_create(args):
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
            _image_create(args, filename)


def _image_create(args, filename):
    image = Image(product=args.product, variant=args.variant, meta=args.meta)
    original_filename = os.path.basename(filename)
    image.set_image(original_filename, open(filename, 'rb'))
    image = CLIENT.images.create(image)
    print(image)


def image_retrieve(args):
    image = CLIENT.images.retrieve(args.uid)
    print(image)


def image_update(args):
    image = CLIENT.images.retrieve(args.uid)

    if args.meta:
        image.meta = args.meta

    CLIENT.images.update(image)
    print(image)


def image_delete(args):
    image = CLIENT.images.retrieve(args.uid)
    CLIENT.images.delete(image)
    print("image deleted")
