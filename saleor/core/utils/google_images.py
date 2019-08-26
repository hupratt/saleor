 
# In[ ]:
from google_images_download import google_images_download   #importing the library
from sqlite3 import Error
import sqlite3
import os, boto3, uuid
from botocore.exceptions import NoCredentialsError
import botocore

# AWS specific

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))

    try:
        s3.upload_file(local_file, bucket, s3_file)
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    bucket_name = bucket_prefix
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': 'eu-west-2'})
    print(bucket_name, "created")
    return bucket_name, bucket_response

def connect_bucket(name):
    try:
        s3resource = boto3.resource('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))
        bucket = s3resource.Bucket(name)
        return bucket

    except botocore.exceptions.ClientError as e:
        print(e)
        return 'does not exist'


# Postgres specific

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def select_all_books(conn):
    cur = conn.cursor()
    cur.execute("SELECT isbn FROM livre")
    rows = cur.fetchall()
    liste_isbn = []
    for row in rows:
        liste_isbn.append(row[0])
    return ",".join(liste_isbn)

# CRUD specific

def lower_quality_images(directory) -> str:
    to_download = list()
    _directory = [i for i in os.listdir(directory)]
    for element in _directory: 
        if os.path.isdir(os.path.join(directory,element)):
            os.chdir(os.path.join(directory,element))
            _file = [i for i in os.listdir(os.path.curdir)]
            os.chdir(directory)
            if len(_file) == 0:
                to_download.append(element)
    return ",".join(to_download)

def ship_to_s3(directory):
    response = dict()
    _directory = [i for i in os.listdir(directory)]
    for element in _directory: 
        if os.path.isdir(os.path.join(directory, element)):
            _file = [i for i in os.listdir(os.path.join(directory, element))]
            if len(_file) > 0:
                response[element] = os.path.join(directory, element, _file[0])
    return response

# main functions

def google_it(placeholders, conn):
    isbn = select_all_books(conn)
    google = google_images_download.googleimagesdownload()
    
    # main download
    arguments = {"keywords":str(isbn), "limit":1, "print_urls":True, "format":"jpg", "size": '>400*300', "output_directory": placeholders}   #creating list of arguments
    paths, _ = google.download(arguments)

    # leftovers
    to_download = lower_quality_images(placeholders)
    arguments = {"keywords":str(to_download), "limit":1, "print_urls":True, "output_directory": placeholders}   #creating list of arguments
    paths, _ = google.download(arguments)

def store_it(bucket_name, placeholders):
    bucket = connect_bucket(bucket_name)
    _json = ship_to_s3(placeholders)
    if bucket == 'does not exist':
        s3_resource = boto3.resource('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))
        first_bucket_name, first_response = create_bucket(bucket_prefix=bucket_name, s3_connection=s3_resource.meta.client)
        for isbn, image_path in _json.items():
            if len(image_path) > 0:
            # upload_to_aws('/home/hugo/Development/saleor/saleor/static/placeholders/saleordemoproduct_cl_boot07_2.png',bucket_name,'saleordemoproduct_cl_boot07_2.png')
                upload_to_aws(image_path, bucket_name, isbn + '.jpg')
    else:
        for isbn, image_path in _json.items():
            # upload_to_aws('/home/hugo/Development/saleor/saleor/static/placeholders/saleordemoproduct_cl_boot07_2.png',bucket_name,'saleordemoproduct_cl_boot07_2.png')
            if len(image_path) > 0:
                upload_to_aws(image_path, bucket_name, isbn + '.jpg')

def rename(placeholders):
    _dir = [i for i in os.listdir(placeholders) if os.path.isdir(os.path.join(placeholders, i))]
    for isbn in _dir:
        img =  [i for i in os.listdir(os.path.join(placeholders, isbn))]
        if len(img)>0:
            filename, file_extension = os.path.splitext(img[0])
            if file_extension not in [".jpg", ".gif", ".png", ".bmp", ".svg", ".webp", ".ico"]:
                filename = img[0]
                file_extension = filename[-4:]
            os.rename(os.path.join(placeholders, isbn, filename + file_extension), os.path.join(placeholders, isbn, isbn + file_extension)) 

def main():
    # DATABASE = "/home/hugo/Downloads/LPP-Master_2019_2019-06-30.db"
    DATABASE = "/home/ubuntu/Dev/LPP-Master_2019_2019-06-30.db"
    # PLACHOLDERS = "/home/hugo/Development/saleor/saleor/static/placeholders"
    PLACHOLDERS = "/home/ubuntu/Dev/saleor/saleor/static/placeholders"
    YOUR_BUCKET_NAME = "lppimagerepo-f1492f08-f236-4a55-afb7-70ded209cb24"

    # create a database connection
    conn = create_connection(DATABASE)
    conn.text_factory = lambda x: str(x, 'latin1')
    with conn:
        google_it(PLACHOLDERS, conn)
        # store_it(YOUR_BUCKET_NAME, PLACHOLDERS)
        rename(PLACHOLDERS)


if __name__ == "__main__":
    main()