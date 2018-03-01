from MessageQueue import MessageBuffer
from sensors import ShakeSensor, ButtonSensor, TemperatureSensor, GeolocationSensor, InactivitySensor
import time


import wifi_connect

#broker = "broker.hivemq.com"
BROKER = "broker.hivemq.com"
TOPIC = "/accelerometer"


queue = MessageBuffer(broker=BROKER, topic=TOPIC)

s = ShakeSensor(queue)
#b = ButtonSensor(queue)
#t = TemperatureSensor(queue, period=2)
#g = GeolocationSensor(queue, period=5)
i = InactivitySensor(queue, period=1, wait_before_sleep=20, time_to_sleep=60)

print('Shake me. Press me')

while True:
#    print('T %f i %f g %s'%(i.value, i.value, str(g.value)))
     time.sleep(3)
     msg = "Inactive %f"%i.value
     print(msg)
