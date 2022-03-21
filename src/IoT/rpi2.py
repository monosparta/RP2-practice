import paho.mqtt.client as mqtt
import json
import datetime
import time
import Adafruit_DHT
import LCD1602
import time

LCD1602.init(0x27, 1)   # init(slave address, background light)
LCD1602.write(0, 0, 'Hi....')
LCD1602.write(1, 1, 'Cherish the time')
time.sleep(2)

 
ISOTIMEFORMAT = '%m/%d %H:%M:%S'
client = mqtt.Client()
client.connect('192.168.168.112', 1883, 60)
 
GPIO_PIN = 4
 
try:
    while True:
        LCD1602.clear()
        humidity, temperature = \
            Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, GPIO_PIN)
        mqttPayload = {
            'temperature': '%.1f'%temperature, 
            'humidity': '%.1f'%humidity,
            'time': datetime.datetime.now().strftime(ISOTIMEFORMAT),
        }
        
        if humidity is not None and temperature is not None:
            # print('temp=%.1f*C, humidity=%.1f%%'%(temperature, humidity))
            print(mqttPayload)
            client.publish("test", json.dumps(mqttPayload))
        else:
            print('read error')
            
        LCD1602.write(0, 0,"Date: {}".format(time.strftime("%Y/%m/%d")))
        LCD1602.write(0, 1,"Time: {}".format(time.strftime("%H:%M:%S")))
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print('keyboard interrupt')
finally:
    LCD1602.clear()