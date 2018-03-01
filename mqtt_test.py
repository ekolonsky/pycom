from mqtt import MQTTClient
#from network import WLAN
#import machine
import time

def sub_cb(topic, msg):
   print(msg)

import wifi_connect


client = MQTTClient("device_id", "broker.hivemq.com", port=1883)

#client.set_callback(sub_cb)
client.connect()
#client.subscribe(topic="youraccount/feeds/lights")

while True:
    print("Sending ON")
    client.publish(topic="youraccount/feeds/lights", msg="ON")
    time.sleep(1)
    print("Sending OFF")
    client.publish(topic="youraccount/feeds/lights", msg="OFF")
    client.check_msg()
