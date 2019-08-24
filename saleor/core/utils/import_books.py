from saleor.product.models import Product, ProductImage, ProductVariant
from prices import Money
import os
from django.core.files import File
from saleor.product.thumbnails import create_product_thumbnails

image_name = "saleordemoproduct_paints_01.png"
image_dir = "saleor/static/placeholders/"


def get_image(image_dir, image_name):
    img_path = os.path.join(image_dir, image_name)
    return File(open(img_path, "rb"), name=image_name)


defaults = {"name":"try out", "weight": "1.0", "category_id": 2, "product_type_id": 2, "attributes": "{}", "price": Money('15.00','EUR')}
product, _ = Product.objects.update_or_create(pk=1, defaults=defaults)

product_image = ProductImage(product=product, image=get_image(image_dir, image_name))
product_image.save()
create_product_thumbnails.delay(product_image.pk)

defaults = {"name":"try out", "weight": "1.0", "product_id": 1, "attributes": "{\"1\": [\"1\"]}", "price_override": Money('15.00','EUR'), "cost_price": Money('1.00','EUR')}
ProductVariant.objects.update_or_create(pk=1, defaults=defaults)
