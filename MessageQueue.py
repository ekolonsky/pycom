import time
from mqtt import MQTTClient, MQTTException
from machine import Timer


#BROKER = "mqtt.avist.io"
#TOPIC  = "/accelerometer"



class MessageBuffer:



    def __init__(self, broker, topic):
        #def settimeout(duration):
        #    pass
        self._broker = broker
        self._topic = topic
        self._client = MQTTClient("pytrack", self._broker, port=1883)
        #self._client.settimeout = settimeout
        self._client.connect()
        self._chrono = Timer.Chrono()
        self._chrono.start()
        print("Connected to MQTT broker %s"%self._broker)
        #self._client.publish(self._topic, "Hello!")
        #_thread.start_new_thread(self._loop, [.1]) # ever loop with small delay
        #self._alarm = Timer.Alarm(self._handler, 0.01 , periodic=True)
        pass

    def send(self, message):
            print('out->', message)
            self._client.publish(self._topic, message)

    def get_timeout(self):
        return self._chrono.read()

#queue = MessageBuffer(broker="mqtt.avist.io", topic="/accelerometer")
