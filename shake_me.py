from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
from network import WLAN
from mqtt import MQTTClient
import machine
import pycom
import time
from MessageQueue import MessageBuffer
from machine import Timer

#broker = "broker.hivemq.com"
BROKER = "mqtt.avist.io"
TOPIC = "/accelerometer"
SSID = "itps-guest" #"Wart-29"
PASS = "parmafree"  # "77599544151"
ACCEL_TRESHOLD = 2000 # shake deteted when acceleration is more than  0.001xG
ACCEL_DURATION = 200  # shake duration is more than 200ms
MAX_TIMEOUT = 20      # time in seconds to wait if nothing happens, then go to go to sleep
TIME_TO_SLEEP = 300   # time to sleep in seconds, then wake up.



print("Connecting to WiFi %s.."%SSID)
wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)
wlan.connect(SSID, auth=(WLAN.WPA2, PASS), timeout=5000)
while not wlan.isconnected():
     machine.idle()
print("Connected to Wifi %s"%SSID)

queue = MessageBuffer(broker=BROKER, topic=TOPIC)

py = Pytrack()
# display the reset reason code and the sleep remaining in seconds
# possible values of wakeup reason are:
# WAKE_REASON_ACCELEROMETER = 1
# WAKE_REASON_PUSH_BUTTON = 2
# WAKE_REASON_TIMER = 4
# WAKE_REASON_INT_PIN = 8

message = "Wake up reason: " + str(py.get_wake_reason())
print(message)
queue.push(message)
print("Approximate sleep remaining: " + str(py.get_sleep_remaining()) + " sec")
time.sleep(0.5)

# enable wakeup source from INT pin
py.setup_int_pin_wake_up(False)



def check_inactivity(alarm):
    global queue, MAX_TIMEOUT, py
    inactivity_time = queue.get_timeout()
    print('Inactivity timer acc:', inactivity_time)
    if inactivity_time > MAX_TIMEOUT:
        print('Going to sleep for %ss'%TIME_TO_SLEEP)
        queue.push('Sleeping..')
        queue._chrono.reset()
        py.setup_sleep(TIME_TO_SLEEP)
        time.sleep(1)
        py.go_to_sleep()
    pass

periodic_checker = Timer.Alarm(check_inactivity, 5, periodic=True)



def handler(pin_o):
  if pin_o():
      a = acc.acceleration() # tuple (ax, ay, az)
      g = (a[0]*a[0] + a[1]*a[1] + a[2]*a[2])**0.5 # abs(a)
      msg = "shake level %f"%g
      queue.push(msg)

# enable activity and also inactivity interrupts, using the default callback handler
py.setup_int_wake_up(True, False)

acc = LIS2HH12()

# enable the activity/inactivity interrupts
# set the accelereation threshold to 2000mG (2G) and the min duration to 200ms

acc.enable_activity_interrupt(ACCEL_TRESHOLD, ACCEL_DURATION,handler=handler)
#acc._user_handler = handler

print('Shake me.')

# go to sleep for 5 minutes maximum if no accelerometer interrupt happens
#py.setup_sleep(60)
#py.go_to_sleep()
