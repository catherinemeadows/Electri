import logging
import boto3
import os
from botocore.exceptions import ClientError

def upload_image(file_name, bucket, object_name=None):
    # Upload file to S3 bucket "senior-design-images"
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

# Upload a sample image
upload_image('image_samples/sample1.jpg', 'senior-design-images', 'sample1.jpg')