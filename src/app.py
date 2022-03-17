from urllib import response
from flask import Flask, render_template, request, jsonify,json,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import false



app = Flask(__name__)

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/test"

db = SQLAlchemy(app)

# 模型( model )定義
class Product4(db.Model):
    __tablename__ = 'product4'
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




# query = Product1.query.filter_by(id='1').first()
# print(query.temperature)
# print(query.humidity)

@app.route('/add',methods=["POST","GET"])
def add():
    sql = """
    INSERT INTO product4(
    temp, humi,time)
    VALUES ('%s', '%s','%s')
"""

    db.engine.execute(sql)
    return "yes"
    
@app.route('/index')
def index1():
    sql = """
    select * from product4
    """
    print(db.engine.execute(sql).fetchall())
    a = db.engine.execute(sql).fetchall()
    b = json.dumps([dict(r) for r in a])
    return render_template('index.html',data = b)

@app.route('/list')
def list():
    sql = """
    select * from product4
    """
    print(db.engine.execute(sql).fetchall())
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

if __name__ == "__main__":
    app.run(debug=True)