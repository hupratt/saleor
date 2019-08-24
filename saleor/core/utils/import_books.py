from saleor.product.models import Product, ProductImage, ProductVariant
from prices import Money
import os, requests, urllib, sqlite3
from django.core.files import File
from saleor.product.thumbnails import create_product_thumbnails
from sqlite3 import Error


def get_image(image_dir, image_name):
    img_path = os.path.join(image_dir, image_name)
    return File(open(img_path, "rb"), name=image_name)


def check_isbn_exists(isbn):
    try:
        pro = ProductVariant.objects.get(sku=isbn)
        return pro
    except ProductVariant.DoesNotExist:
        return False


def get_book_cover_google_url(name, isbn):
    url = "https://www.googleapis.com/books/v1/volumes?q=" + isbn
    response = requests.get(url).json()
    if response['totalItems'] != 0:
        image_url = response['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        os.chdir("/home/hugo/Development/saleor/saleor/static/placeholders")
        urllib.request.urlretrieve(image_url, name+".jpg")

def create_product(quantity, name, price, weight, image_name, image_dir, isbn, attr, pk):
    pro_variant_instance = check_isbn_exists(isbn)
    if isinstance(pro_variant_instance, ProductVariant):
        pk = pro_variant_instance.pk
        quantity = pro_variant_instance.quantity
        quantity += 1
        variant_defaults = {"name":name, "weight": weight, "product_id": pk, "attributes": attr, "price_override": Money(price,'EUR'), "cost_price": Money(price,'EUR'), "sku":isbn, "quantity": quantity}
        ProductVariant.objects.update_or_create(pk=pk, defaults=variant_defaults)
    else:
        product_defaults = {"name":name, "weight": weight, "category_id": 2, "product_type_id": 2, "attributes": "{}", "price": Money(price,'EUR')}
        product, _ = Product.objects.update_or_create(pk = pk, defaults=product_defaults)
        product_image = ProductImage(product=product, image=get_image(image_dir, image_name))
        product_image.save()
        create_product_thumbnails.delay(product_image.pk)
        variant_defaults = {"name":name, "weight": weight, "product_id": pk, "attributes": attr, "price_override": Money(price,'EUR'), "cost_price": Money(price,'EUR'), "sku":isbn, "quantity": quantity}
        ProductVariant.objects.update_or_create(pk=pk, defaults=variant_defaults)


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def select_all_books(conn):

    cur = conn.cursor()
    cur.execute("SELECT titre, isbn, prix FROM livre")
 
    rows = cur.fetchall()
    # name = "Um Museu do Outro Mundo"
    # price = '10.00'
    # image_name = "saleordemoproduct_paints_01.png"
    # image_name ="Um Museu do Outro Mundo.jpg"
    # image_name = "Paula Rego.jpg"
    image_dir = "saleor/static/placeholders/"
    # isbn = '0553283685'
    # 1 for English attr = {"1": ["1"]}
    # 2 for Portuguese attr = {"1": ["2"]}
    attr = {"1": ["2"]}
    weight = "0.1"
    # pk = 1
    quantity = 1
    for counter, row in enumerate(rows):
        name, isbn, price = row
        price = str(price) + '0'
        price = price.replace(",",'.')
        image_name = name + 'jpg'
        pk = counter + 1
        get_book_cover_google_url(name = name, isbn = isbn)
        create_product(name = name, price = price, weight = weight, 
               image_name = image_name, image_dir = image_dir, 
               isbn = isbn, attr = attr, pk = pk, quantity = quantity)

database = "/home/hugo/Downloads/LPP-Master_2019_2019-06-30.db"

# create a database connection
conn = create_connection(database)
conn.text_factory = lambda x: str(x, 'latin1')
# conn.text_factory = str
with conn:
    select_all_books(conn)
 
