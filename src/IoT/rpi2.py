import paho.mqtt.client as mqtt
import json
import datetime
import time
import Adafruit_DHT
import LCD1602
from multiprocessing import Process
import time
# test
ISOTIMEFORMAT = '%m/%d %H:%M:%S'
client = mqtt.Client()
client.connect('192.168.168.112', 1883, 60)

def i2cHandler():
    def on_message(client, userdata, msg):
        decodedMessage = str(msg.payload.decode("utf-8"))
        content = json.loads(decodedMessage)
        # print(content['temperature'], content['humidity'], content['time'])
        LCD1602.write(0, 0,"<total 16>")
        LCD1602.write(0, 1,"<en words>")

    try:
        # using "$ i2cdetect -y 1" to look for i2c-address
        LCD1602.init(0x3f, 1)   # init(slave address, background light)
        LCD1602.write(0, 0, 'Hi....')
        LCD1602.write(1, 1, 'Cherish the time')
        time.sleep(10)
        client.subscribe('i2c')
        client.on_message = on_message
        client.loop_forever()
    except:
        pass

def dh11Detect():
    try:
        while True:
            humidity, temperature = \
                Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 17)
            mqttPayload = {
                'temperature': '%.1f'%temperature, 
                'humidity': '%.1f'%humidity,
                'time': datetime.datetime.now().strftime(ISOTIMEFORMAT),
            }
            
            if humidity is not None and temperature is not None:
                print(mqttPayload)
                client.publish("dh11", json.dumps(mqttPayload))
            else:
                print('read error')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('keyboard interrupt')  

if __name__ == '__main__': 
    Process(target=i2cHandler).start()
    dh11Detect()
