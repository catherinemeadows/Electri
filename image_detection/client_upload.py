import boto3
from decimal import Decimal
import time
import json
import random
import string
path ='images/c4.jpg'
region = 'us-east-1'
s3client = boto3.client('s3', region_name=region)
s3client.upload_file(path, 'electri-image-uploads', path)
SFclient = boto3.client('stepfunctions')
exec_name = ''.join(random.choice(string.ascii_lowercase) for i in range(40))
response = SFclient.start_execution(
    stateMachineArn='arn:aws:states:us-east-1:497100321969:stateMachine:Electri-ProcessImageUploadWorkflow',
    input= """{
    "latitude":38.900303,
    "longitude":-77.047602,
    "img_path":"images/c4.jpg",
    "execution_name": \"%s\"
    }""" % exec_name
)

exec_name = ''.join(random.choice(string.ascii_lowercase) for i in range(40))
path ='images/c6.jpg'
s3client.upload_file(path, 'electri-image-uploads', path)
response = SFclient.start_execution(
    stateMachineArn='arn:aws:states:us-east-1:497100321969:stateMachine:Electri-ProcessImageUploadWorkflow',
    input= """{
    "latitude":38.900303,
    "longitude":-77.049602,
    "img_path":"images/c6.jpg",
    "execution_name": \"%s\"
    }""" % exec_name
)


