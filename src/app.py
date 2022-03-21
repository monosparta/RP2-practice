from cgitb import text
import json
from re import S
from time import sleep
from urllib import response
from flask import Flask, render_template, request, jsonify,json,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json, time, datetime
import pysolr
import pandas as pd

from sqlalchemy import false

import paho.mqtt.client as mqtt
from multiprocessing import Process
import mysql.connector


ISOTIMEFORMAT = '%m/%d %H:%M:%S'
client = mqtt.Client()
client.connect('192.168.168.112', 1883, 60)


app = Flask(__name__)

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/flask"

db = SQLAlchemy(app)

# 模型( model )定義
class dh11(db.Model):
    __tablename__ = 'dh11'
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(
        db.VARCHAR(30),  nullable=False)
    humi = db.Column(
        db.VARCHAR(30),  nullable=False)
    time = db.Column(
        db.VARCHAR(30), nullable=False)
    


    def __init__(self, temp, humi, time):
        self.temp = temp
        self.humi = humi
        self.time = time
    
@app.route('/index')
def index1():
    sql = """
    select * from dh11 
    """
    # print(db.engine.execute(sql).fetchall())
    a = db.engine.execute(sql).fetchall()
    b = json.dumps([dict(r) for r in a])
    return render_template('index.html',data = b)

@app.route('/test',methods=['POST','GET'])
def test():
    return "ok"

def process_json(data):
	return data

@app.route('/list')
def list():
    sql = """
    select * from (select * from dh11 order by id desc limit 25) as preProcess GROUP BY time order by id LIMIT 10;
    """
    # print(db.engine.execute(sql).fetchall())
    a = db.engine.execute(sql).fetchall()
    return json.dumps([dict(r) for r in a])
@app.route('/')
def index():
    # Create data
    #a = Product1.query.all()
    db.create_all()
    #b = json.dumps([dict(r) for r in a])
    
#list(a.id())
    return "ok"
@app.route('/i2cpb',methods=['POST'])
def i2cpb1():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        mqttPayload = {
            'message': json                
        }
        
        global client
        client.publish("i2c", json.dumps(mqttPayload))
        
    else:
        print("fail") 
    

mysqlConnection = None    
def on_message(client, userdata, msg):
    decodedMessage = str(msg.payload.decode("utf-8"))
    content = json.loads(decodedMessage)
    # print(content['temperature'], content['humidity'], content['time'])
    global mysqlConnection
    cursor = mysqlConnection.cursor()
    # cursor.execute('select * from DH11 order by id desc limit 1')
    # lastRecord = cursor.fetchall()
    # print('last record', lastRecord[0][3])

    queryString = 'insert into `DH11` (`temp`,`humi`,`time`) \
        values ("%s", "%s", "%s");'%(str(content['temperature']), str(content['humidity']), str(content['time']))
    # print(queryString)
    cursor.execute(queryString)
    mysqlConnection.commit()


def mqttHandlerAndMysql():
    global mysqlConnection
    mysqlConnection = mysql.connector.connect(host='127.0.0.1',
                                         database='flask',
                                         user='root',
                                         password='')
        
    global client
    client.subscribe("dh11")
    client.on_message = on_message
    client.loop_forever()

if __name__ == "__main__":
    Process(target=mqttHandlerAndMysql).start()
    app.run(host='0.0.0.0', debug=True, )