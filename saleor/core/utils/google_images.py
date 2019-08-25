 
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
    finally:
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


def main():
    database = "/home/hugo/Downloads/LPP-Master_2019_2019-06-30.db"
    # create a database connection
    conn = create_connection(database)
    conn.text_factory = lambda x: str(x, 'latin1')
    # conn.text_factory = str
    with conn:
        isbn = select_all_books(conn)
        google = google_images_download.googleimagesdownload()   #class instantiation
        arguments = {"keywords":str(isbn), "limit":1, "print_urls":True,"format":"jpg", "size": '>800*600', "output_directory": "/home/hugo/Development/saleor/saleor/static/placeholders"}   #creating list of arguments
        paths, _ = google.download(arguments)   #passing the arguments to the function

        YOUR_BUCKET_NAME = "lppimagerepo-f1492f08-f236-4a55-afb7-70ded209cb24"
        bucket = connect_bucket(YOUR_BUCKET_NAME)
        if bucket == 'does not exist':
            s3_resource = boto3.resource('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))
            first_bucket_name, first_response = create_bucket(bucket_prefix=YOUR_BUCKET_NAME, s3_connection=s3_resource.meta.client)
            for isbn, image_path in paths.items():
                upload_to_aws(image_path[0], YOUR_BUCKET_NAME, isbn+'.jpg')
        else:
            for isbn, image_path in paths.items():
                upload_to_aws(image_path[0], YOUR_BUCKET_NAME, isbn+'.jpg')

if __name__ == "__main__":
    main(NAME)