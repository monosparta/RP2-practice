import paho.mqtt.client as mqtt
import json
import datetime
import time
import Adafruit_DHT

 
ISOTIMEFORMAT = '%m/%d %H:%M:%S'
client = mqtt.Client()
client.connect('192.168.168.112', 1883, 60)
 
GPIO_PIN = 4
 
try:
    while True:
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
        time.sleep(0.05)
        
except KeyboardInterrupt:
    print('keyboard interrupt')