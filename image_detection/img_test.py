import boto3
from decimal import Decimal
import time
from boto3.dynamodb.conditions import Key, Attr
path ='cars/c3.jpg'
region = 'us-east-1'
client = boto3.client('s3', region_name=region)
dynamodb = boto3.resource('dynamodb', region_name=region)
dynamo_client = boto3.client('dynamodb', region_name=region)
table = dynamodb.Table('Alerts')
response = dynamo_client.execute_statement(
    Statement='SELECT * FROM "Alerts" WHERE "status" = 0'
)
print(response)
for i in response['Items']:
    print(i['color'])
#table = dynamodb.Table('Input_Packets')
#response = table.put_item(
#    Item={
#        'img_path': path,
#        'timestamp': Decimal(int(time.time()))
#    }
#)
#client.upload_file(path, 'senior-design-images', path)
