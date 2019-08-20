from saleor.product.models import Product, ProductImage
from prices import Money

defaults = {"name":"try out 2", "weight": "1.0", "category_id": 2, "product_type_id": 2, "attributes": "{}", "price": Money('15.00','EUR')}
product = Product.objects.update_or_create(pk=2, defaults=defaults)

product_image = ProductImage(product=product, image=get_image())
product_image.save()
create_product_thumbnails.delay(product_image.pk)