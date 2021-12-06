import boto3
from decimal import Decimal
import time
path ='cars/car5.jpg'
region = 'us-east-1'
client = boto3.client('s3', region_name=region)
dynamodb = boto3.resource('dynamodb', region_name=region)
print(Decimal(int(time.time())))
table = dynamodb.Table('Input_Packets')
response = table.put_item(
    Item={
        'img_path': path,
        'timestamp': Decimal(int(time.time()))
    }
)
client.upload_file(path, 'senior-design-images', path)
