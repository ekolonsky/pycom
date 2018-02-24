from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
import pycom
import time

broker = "broker.hivemq.com"
topic = "/accelerometer"
SSID = "Wart-29"
PASS = "77599544151"


from network import WLAN
from mqtt import MQTTClient
import machine

def settimeout(duration):
    pass

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)
wlan.connect(SSID, auth=(WLAN.WPA2, PASS), timeout=5000)

while not wlan.isconnected():
     machine.idle()

print("Connected to Wifi\n")
client = MQTTClient("pytrack", broker, port=1883)
client.settimeout = settimeout
client.connect()
client.publish(topic, "Hello")
client.disconnect()

py = Pytrack()
# py = Pysense()


def handler(pin_o):
  if pin_o():
    count +=1
    msg='ON'
  else:
    msg = 'OFF'
  client.connect()
  client.publish(topic, msg)
  client.disconnect()
  print(msg)

# enable activity and also inactivity interrupts, using the default callback handler
py.setup_int_wake_up(True, False)

acc = LIS2HH12()

# enable the activity/inactivity interrupts
# set the accelereation threshold to 2000mG (2G) and the min duration to 200ms

acc.enable_activity_interrupt(2000, 200)
acc._user_handler = handler

print('Shake me..')
