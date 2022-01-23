import boto3
import os
from flask import request
from flask import Flask
app = Flask(__name__)
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

@app.route('/get_matches_current', methods=['POST'])
def get_matches_current():
    results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""
            SELECT * 
            FROM alerts 
            INNER JOIN matches ON matches.alert_id = alerts.id 
            INNER JOIN image_info ON matches.img_id = image_info.id 
            WHERE alerts.alert_status = 0;
        """
    )
    print(results.keys())
    records = results['records']
    columns = results['columnMetadata']
    
    #print(records)
    
    for record in records:
        for i, val in enumerate(columns):
            print(columns[i]['name']+str(record[i]))
        #download_image_if_needed(record['img_path'])
    return str(records)

@app.route('/get_matches_archived', methods=['POST'])
def get_matches_archived():
    alertId = request.form['alert_id']
    query_results = None
    if alertId:
        results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""
        SELECT (
            image_info.id,
            image_info.img_path,
            image_info.latitude,
            image_info.longitude,
            alerts.id  
        ) FROM 
        alerts JOIN matches ON matches.alert_id = alerts.id 
        JOIN image_info ON matches.img_id = image_info.id 
        WHERE alerts.alert_id = %d;
        """ % alertId)
        
        query_results =results['records']
    else:
        results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""
        SELECT (
            image_info.img_id AS img_id,
            image_info.img_path AS img_path,
            image_info.latitude AS latitude,
            image_info.longitude AS longitude,
            alerts.alert_id AS alert_id
        ) FROM 
        alerts JOIN matches ON matches.alert_id = alerts.id 
        JOIN image_info ON matches.img_id = image_info.id;
        """)
        query_results = results['records']
        print(query_results)
    return query_results

@app.route('/insert_alert', methods=['POST'])
def insert_alert():
    results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""INSERT INTO alerts VALUES (%s,%s)""" % (request.form['email'],request.form['password']))
    return str(results)

@app.route('/login', methods=['POST'])
def login():
    results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql ="""SELECT * FROM users FROM users WHERE email = %s AND password = %s;""" % (request.form['email'],request.form['password']))
    return str(results)

@app.route('/register', methods=['POST'])
def register():
    results = rds_data.execute_statement(
        resourceArn = ARN,
        secretArn = SECRET_ARN,
        database = DBNAME,
        sql=
        """INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s);""" % 
        (
            request.form['username'],
            request.form['user_password'],
            request.form['fname'],
            request.form['lname'],
            request.form['email'],
            request.form['organization']
        )
    )
    query_results = str(results)
    return query_results

def download_image_if_needed(img_path):
    if not os.path.isfile('dist/assets/'+img_path):
        with open('dist/assets/'+img_path, 'wb') as f:
            s3.download_fileobj('electri-upload-images', img_path, f)
        