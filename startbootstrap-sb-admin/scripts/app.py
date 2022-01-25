import json
import time
import boto3
import os
from flask import request
from flask import Flask
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)
ENDPOINT="electri-database.c0eyquvqg5yr.us-east-1.rds.amazonaws.com"
PORT="3306"
USER="admin"
PASSWORD = "electri!"
REGION="us-east-1"
DBNAME="electri_db"
ARN = "arn:aws:rds:us-east-1:497100321969:cluster:electridb"
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:497100321969:secret:rds-db-credentials/cluster-LMOUBFEGQDIUC3YMT3DCVX54MM/admin-sEVflU"
#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
rds_data = session.client('rds-data')
s3 = boto3.client('s3')
if not os.path.exists("dist/assets/images"):
    os.mkdir("dist/assets/images")
    
tokens = {}
username_to_token = {}

@app.route('/getMatches', methods=['POST'])
def get_matches_current():
    ok, msg = checkLogin()
    if not ok:
        return {
            "Code":500,
            "message":msg
        }
    data = json.loads(request.get_data())
    alerts = data.get('alerts')
    results = None
    if alerts:
        results = rds_data.execute_statement(
            resourceArn = ARN,
            secretArn = SECRET_ARN,
            database = DBNAME,
            sql ="""
                SELECT alerts.id,image_info.img_path,image_info.latitude,image_info.longitude 
                FROM alerts 
                JOIN matches ON matches.alert_id = alerts.id 
                JOIN image_info ON matches.img_id = image_info.id 
                WHERE alerts.alert_status = 1 AND alerts.id in %s;
            """ % (tuple(alerts))
        )
    else:
        results = rds_data.execute_statement(
            resourceArn = ARN,
            secretArn = SECRET_ARN,
            database = DBNAME,
            sql ="""
                SELECT alerts.id,image_info.img_path,image_info.latitude,image_info.longitude 
                FROM alerts 
                JOIN matches ON matches.alert_id = alerts.id 
                JOIN image_info ON matches.img_id = image_info.id 
                WHERE alerts.alert_status = 1;
            """
        )
        
    return {
        "code": 200,
        "message": "OK",
        "data" : parseMatches(results['records'])
    }

@app.route('/get_matches_archived', methods=['POST'])
def get_matches_archived():
    ok, msg = checkLogin()
    data = json.loads(request.get_data())
    if not ok:
        return {
            "Code":500,
            "message":msg
        }
    records = None
    if 'alert_id' in data:
        alertId = data['alert_id']
        results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""
            SELECT alerts.id,image_info.img_path,image_info.latitude,image_info.longitude 
            FROM alerts 
            JOIN matches ON matches.alert_id = alerts.id 
            JOIN image_info ON matches.img_id = image_info.id 
            WHERE alerts.alert_id = %d;
        """ % alertId)
        
        records =results['records']
    else:
        results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""
            SELECT alerts.id,image_info.img_path,image_info.latitude,image_info.longitude 
            FROM alerts 
            JOIN matches ON matches.alert_id = alerts.id 
            JOIN image_info ON matches.img_id = image_info.id;
        """)
        records = results['records']
        return {
        "code": 200,
        "message": "OK",
        "data" : parseMatches(records)
    }

@app.route('/insert_alert', methods=['POST'])
def insert_alert():
    data = json.loads(request.get_data())
    ok, msg = checkLogin()
    if not ok:
        return {
            "Code":500,
            "message":msg
        }
    results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""
            INSERT INTO alerts  (
                alert_status,
                city,
                alert_state,
                latitude,
                longitude,
                license_plate,
                make,
                model,
                vehicle_year,
                color
            ) 
            VALUES 
            (%d,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" % (
                data.get('alert_staus'),
                data.get('city'),
                data.get('alert_state'),
                data.get('latitude'),
                data.get('longitude'),
                data.get('license_plate'),
                data.get('make'),
                data.get('model'),
                data.get('vehicle_year'),
                data.get('color'),
                ))
    return {
        "code": 200,
        "message": "OK"
    }

@app.route('/get_alerts', methods=['POST'])
def get_alerts():
    ok, msg = checkLogin()
    data = json.loads(request.get_data())
    if not ok:
        return {
            "Code":500,
            "message":msg
        }
    results = None
    if 'alert_status' in data:
        results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""SELECT * FROM alerts WHERE alert_status = %s;""" % (data['alert_status']))
    else:
        results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""SELECT * FROM alerts;""" )
    alerts = {
        'alerts':[]
    }
    for record in results['records']:
        alert = []
        for col in record:
            alert.append(col[list(col.keys())[0]])
        alerts['alerts'].append(alert)
    return {
        "code": 200,
        "message": "OK",
        "data" : alerts
    }

@app.route('/verifyLogin', methods=['POST'])
def verifylogin():
    
    ok, msg = checkLogin()
    return {
        "Code":200,
        "message":msg,
        "data":ok
    }
    
@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.get_data())
    username = data['username']
    password = data['password']
    if not username or not password:
        print(username, password)
        print("nope")
        return {
            "code": 400,
            "message": "Check Input"
        }
    sql_statement = """SELECT * FROM user WHERE username = \"%s\" AND user_password = \"%s\";""" % (username,password)
    results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql =sql_statement)
    if len(results['records']) != 1:
        print("oops")
        return {
            "Code":200,
            "Message":"Invalid Login"
        }
    token = None
    if results['records'][0][0]['stringValue'] in username_to_token:
        token = username_to_token[results['records'][0][0]['stringValue']]
    else:
        token = ''.join(random.choice(string.ascii_lowercase) for i in range(50))
        username_to_token[results['records'][0][0]['stringValue']] = token
    tokens[token] = time.time()+3600
    return {
        "code":200,
        "message":"OK",
        "data": token
    }
    
@app.route('/logout', methods=['POST'])
def logout():
    data = json.loads(request.get_data())
    token = data.get('token')
    if not token:
        return {
            "code" :400,
            "message": "Internal Error"
        }
    if token in list(username_to_token.values()):
        keys = list(username_to_token.keys())
        key = keys[list(username_to_token.values()).index(token)]
        del username_to_token[key]
    if token in tokens:
        del tokens[token]
    return {
        "code": 200,
        "message":"OK"
    }
        
@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.get_data())
    ok, msg = checkLogin()
    if not ok:
        return {
            "Code":500,
            "message":msg
        }
    results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql=
        """INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s);""" % 
        (
            data.get('username'),
            data.get('user_password'),
            data.get('fname'),
            data.get('lname'),
            data.get('email'),
            data.get('organization')
        )
    )
    return {
        "code": 200,
        "message": "OK",
    }

def download_image_if_needed(img_path):
    if not os.path.isfile('dist/assets/'+img_path):
        with open('dist/assets/'+img_path, 'wb') as f:
            s3.download_fileobj('electri-image-uploads', img_path, f)
       
def parseMatches(records): 
    matches = []
    for record in records:
        match_data = {
            "alert_id": record[0]['longValue'],
            "img_path": record[1]['stringValue'],
            "latitude": float(record[2]['stringValue']),
            "longitude": float(record[3]['stringValue'])
        }
        download_image_if_needed(record[1]['stringValue'])
        matches.append(match_data)
    return matches

def checkLogin():
    data = json.loads(request.get_data())
    token = data.get('token')
    if not token:
        return False, 'Internal error'
    
    if data['token'] not in list(tokens.keys()):
        return False, 'Invalid login'
    elif time.time() > tokens[data['token']]:
        return False, 'Login Expired, please login again'
    tokens[data['token']] = time.time() + 3600
    return True, ''
    
            