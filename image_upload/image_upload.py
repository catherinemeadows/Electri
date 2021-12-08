import logging
import boto3
import os
from botocore.exceptions import ClientError
import time

logging.basicConfig(filename='image_upload.log', level=logging.DEBUG)

def uploadImage(file_name, bucket, object_name=None):
    # Upload file to S3 bucket
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Create client object
    s3 = boto3.client('s3')

    # Attempt to upload an image to S3
    try:
        response = s3.upload_file(file_name, bucket, 'cars/' + object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def downloadImage(object_name, bucket, file_name=None):
    # Download file from S3 bucket
    if file_name is None:
        file_name = object_name
    
    # Create client object
    s3 = boto3.client('s3')

    # Attempt to download an image from S3
    try:
        response = s3.download_file(bucket, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def deleteImage(object_name, bucket):
    # Delete file from S3 bucket
    # Create client object
    s3 = boto3.client('s3')

    # Attempt to delete an image from S3
    try:
        response = s3.delete_object(Bucket = bucket, Key = object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def createImageDDBItem(path, timestamp, latitude, longitude, ddb_table=None):
    # Create a new DDB item to represent an uploaded image
    ddb = boto3.client('dynamodb')

    # Default to the images table
    if ddb_table is None:
        ddb_table = 'Input_Packets'

    # Attempt to create an item in DynamoDB
    try:
        response = ddb.put_item(
            TableName = ddb_table,
            Item = {
                'timestamp': {
                    'N': timestamp
                },
                'img_path': {
                    'S': path
                },
                'lon': {
                    'N': longitude
                },
                'lat': {
                    'N': latitude
                }
            }
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True

#
# EXAMPLE API CALLS
#

# Upload a sample image
uploadImage('image_samples/c3.jpg', 'senior-design-images', 'c3.jpg')
# Download the sample image
# downloadImage('cars/upload.jpg', 'senior-design-images', 'image_samples/download.jpg')
# Create the sample image DDB item
createImageDDBItem('cars/c3.jpg', str(int(time.time())), '38.900071', '-77.040473', 'Input_Packets')
# Delete the image from S3
# deleteImage('cars/upload.jpg', 'senior-design-images')