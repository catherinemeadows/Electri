from turtle import down
import mysql.connector
import sys
import boto3
import os
from flask import app, request
import flask
from flask import Flask
app = Flask(__name__)
ENDPOINT="electri-database.c0eyquvqg5yr.us-east-1.rds.amazonaws.com"
PORT="3306"
USER="admin"
PASSWORD = "electri!"
REGION="us-east-1"
DBNAME="electri_db"

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')
conn =  mysql.connector.connect(host=ENDPOINT, user=USER, passwd=PASSWORD, port=PORT, database=DBNAME)
cur = conn.cursor()
s3 = boto3.client('s3')

@app.route('/get_matches_current', methods=['POST'])
def get_matches_current():
    query_results = None
    cur.execute("""
    SELECT (
        image_info.img_id AS img_id,
        image_info.img_path AS img_path,
        image_info.latitude AS latitude,
        image_info.longitude AS longitude,
        alerts.alert_id AS alert_id
    ) FROM 
    alerts JOIN matches ON matches.alert_id = alerts.alert_id 
    JOIN image_info ON matches.img_id = image_info.img_id 
    WHERE alerts.alert_status = 0;
    """)
    query_results = cur.fetchall()
    
    for result in query_results:
        download_image_if_needed(result[])
    return str(query_results)

@app.route('/get_matches_archived', methods=['POST'])
def get_matches_archived():
    alertId = request.form['alert_id']
    query_results = None
    if alertId:
        cur.execute("""
        SELECT (
            image_info.img_id AS img_id,
            image_info.img_path AS img_path,
            image_info.latitude AS latitude,
            image_info.longitude AS longitude,
            alerts.alert_id AS alert_id
        ) FROM 
        alerts JOIN matches ON matches.alert_id = alerts.alert_id 
        JOIN image_info ON matches.img_id = image_info.img_id 
        WHERE alerts.alert_id = %d;
        """ % alertId)
        query_results = cur.fetchall()
        print(query_results)
    else:
        cur.execute("""
        SELECT (
            image_info.img_id AS img_id,
            image_info.img_path AS img_path,
            image_info.latitude AS latitude,
            image_info.longitude AS longitude,
            alerts.alert_id AS alert_id
        ) FROM 
        alerts JOIN matches ON matches.alert_id = alerts.alert_id 
        JOIN image_info ON matches.img_id = image_info.img_id;
        """)
        query_results = cur.fetchall()
        print(query_results)
    return query_results

@app.route('/insert_alert', methods=['POST'])
def insert_alert():
    cur.execute("""INSERT INTO alerts VALUES (%s,%s)""" % (request.form['email'],request.form['password']))
    query_results = cur.fetchall()
    return query_results

@app.route('/login', methods=['POST'])
def login():
    cur.execute("""SELECT * FROM users FROM users WHERE email = %s AND password = %s;""" % (request.form['email'],request.form['password']))
    query_results = cur.fetchall()
    return query_results

@app.route('/register', methods=['POST'])
def register():

    cur.execute("""INSERT INTO users VALUES ()""")
    query_results = cur.fetchall()
    return query_results

def download_image_if_needed(img_path):
    if not os.path.isfile('dist/assets/'+img_path):
        with open('dist/assets/'+img_path, 'wb') as f:
            s3.download_fileobj('electri-upload-images', img_path, f)
        