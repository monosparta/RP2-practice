import time
import Adafruit_DHT
 
GPIO_PIN = 4
 
try:
    while True:
        h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, GPIO_PIN)
        if h is not None and t is not None:
            print('temp=%.1f*C, humidity=%.1f%%'%(t, h))
        else:
            print('read error')
        time.sleep(0.05)
        
except KeyboardInterrupt:
    print('keyboard interrupt')