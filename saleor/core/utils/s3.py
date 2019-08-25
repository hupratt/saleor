import os, boto3, uuid
import uuid
from botocore.exceptions import NoCredentialsError
import botocore


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name


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
            
    

YOUR_BUCKET_NAME = "lppimagerepo-f1492f08-f236-4a55-afb7-70ded209cb24"
bucket = connect_bucket(YOUR_BUCKET_NAME)
local_file = '/home/hugo/Development/saleor/saleor/static/placeholders/9789896267940/1.32799139._UY1176_SS1176_.jpg'

if bucket == 'does not exist':
    s3_resource = boto3.resource('s3', aws_access_key_id=os.environ.get('S3_ACCESS_KEY'), aws_secret_access_key=os.environ.get('S3_SECRET_KEY'))
    first_bucket_name, first_response = create_bucket(bucket_prefix=YOUR_BUCKET_NAME, s3_connection=s3_resource.meta.client)
    first_file_name = create_temp_file(300, 'firstfile.txt', 'f')   
    first_object = s3_resource.Object(bucket_name=first_bucket_name, key=first_file_name)
    first_object.upload_file(first_file_name)
    uploaded = upload_to_aws(local_file, bucket, 'image_0.jpg')

else:
    first_file_name = create_temp_file(300, 'firstfile.txt', 'f')   
    first_object = bucket.Object(bucket_name=YOUR_BUCKET_NAME, key=first_file_name)
    first_object.upload_file(first_file_name)
    uploaded = upload_to_aws(local_file, YOUR_BUCKET_NAME, 'image_0.jpg')



# upload_to_aws('/home/hugo/Development/saleor/saleor/static/placeholders/9789896267940/1.32799139._UY1176_SS1176_.jpg', YOUR_BUCKET_NAME, 'image_0.jpg')

