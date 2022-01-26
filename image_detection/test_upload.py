import boto3
from decimal import Decimal
import time
import json
import random
import string
path ='images/c6.jpg'
region = 'us-east-1'
client = boto3.client('s3', region_name=region)
client.upload_file(path, 'electri-image-uploads', path)
client = boto3.client('stepfunctions')
exec_name = ''.join(random.choice(string.ascii_lowercase) for i in range(40))
response = client.start_execution(
    stateMachineArn='arn:aws:states:us-east-1:497100321969:stateMachine:Electri-ProcessImageUploadWorkflow',
    input= """{
    "latitude":38.9005,
    "longitude":-77.4123,
    "img_path":"images/c6.jpg",
    "execution_name": \"%s\"
    }""" % exec_name
)


