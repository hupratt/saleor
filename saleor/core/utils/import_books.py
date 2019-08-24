from saleor.product.models import Product, ProductImage, ProductVariant
from prices import Money
import os
from django.core.files import File
from saleor.product.thumbnails import create_product_thumbnails


def get_image(image_dir, image_name):
    img_path = os.path.join(image_dir, image_name)
    return File(open(img_path, "rb"), name=image_name)

# name = "Um Museu do Outro Mundo"
name = "Paula Rego"
price = '10.00'
# image_name = "saleordemoproduct_paints_01.png"
# image_name ="Um Museu do Outro Mundo.jpg"
image_name = "Paula Rego.jpg"
image_dir = "saleor/static/placeholders/"
isbn = 9789899568792
# 1 for English attr = {"1": ["1"]}
# 2 for Portuguese attr = {"1": ["2"]}
attr = {"1": ["2"]}
weight = "0.1"
pk = 1
quantity = 1
get_book_cover = "https://www.googleapis.com/books/v1/volumes?q="+str(isbn)

def create_product(quantity = quantity, name = name, price = price, weight = weight, image_name = image_name, image_dir = image_dir, isbn = isbn, attr = attr, pk = pk):
    product_defaults = {"name":name, "weight": weight, "category_id": 2, "product_type_id": 2, "attributes": "{}", "price": Money(price,'EUR')}
    product, _ = Product.objects.update_or_create(pk = pk, defaults=product_defaults)
    product_image = ProductImage(product=product, image=get_image(image_dir, image_name))
    product_image.save()
    create_product_thumbnails.delay(product_image.pk)
    variant_defaults = {"name":name, "weight": weight, "product_id": pk, "attributes": attr, "price_override": Money('15.00','EUR'), "cost_price": Money('1.00','EUR'), "sku":isbn, "quantity": quantity}
    ProductVariant.objects.update_or_create(pk=pk, defaults=variant_defaults)

create_product(name = name, price = price, weight = weight, 
               image_name = image_name, image_dir = image_dir, 
               isbn = isbn, attr = attr, pk = pk, quantity = quantity)