# RP2-practice
## 安裝套件
flask-sqlalchemy套件
```
$ pip install flask-sqlalchemy
```
flask套件
```
$ pip install flask
```
paho-mqtt套件
```
$ pip install paho-mqtt
```
multiprocess套件
```
$ pip install multiprocess
```
mysql-connector套件
```
$ python -m pip install mysql-connector
```

## 套件引入
flask相關套件
```
from flask import Flask, render_template,json
```
flask_sqlalchemy套件
```
from flask_sqlalchemy import SQLAlchemy
```
paho.mqtt.clint套件
```
import paho.mqtt.client as mqtt
```
multiprocessing套件
```
from multiprocessing import Process
```
mysql.connector套件
```
import mysql.connector
```
## 使用設備
Raspberry Pi 2

DHT11

I2C 1602


## 執行腳本
1. 利用user1(:user1)身分ssh登入樹梅派後切換使用者為pi(:raspberry)
2. 進入user1中執行rpi2.py，即可成功
3. :warning: 若有任何error則尋求google協助
