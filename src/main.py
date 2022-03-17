from urllib import response
from flask import Flask, render_template, request, jsonify,json,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost:3306/test"

db = SQLAlchemy(app)

# 模型( model )定義
class Product1(db.Model):
    __tablename__ = 'product1'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(
        db.VARCHAR(30), unique=True, nullable=False)
    humidity = db.Column(
        db.VARCHAR(30), unique=True, nullable=False)
    time = db.Column(
        db.DateTime, default=datetime.now)
    


    def __init__(self, temperature, humidity, time):
        self.temperature = temperature
        self.humidity = humidity
        self.time = time




# query = Product1.query.filter_by(id='1').first()
# print(query.temperature)
# print(query.humidity)

@app.route('/add')
def add():
    product_max = Product1('25', '75','')
    db.session.add(product_max)
    db.session.commit()
    return "yes"
    
@app.route('/home')
def home():
    sql = """
    select * from product1
    """
    print(db.engine.execute(sql).fetchall())
    a = db.engine.execute(sql).fetchall()
    return render_template('home.html',data = a)

@app.route('/list')
def list():
    sql = """
    select * from product1
    """
    print(db.engine.execute(sql).fetchall())
    a = db.engine.execute(sql).fetchall()
    return json.dumps([dict(r) for r in a])
@app.route('/')
def index():
    # Create data
    a = Product1.query.all()
    db.create_all()
    b = json.dumps([dict(r) for r in a])
    
#list(a.id())
    return render_template('index.html',data = a)

if __name__ == "__main__":
    app.run(debug=True)