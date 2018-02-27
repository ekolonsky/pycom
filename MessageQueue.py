import _thread
import time
from mqtt import MQTTClient, MQTTException
from machine import Timer


#BROKER = "mqtt.avist.io"
#TOPIC  = "/accelerometer"



class MessageBuffer:



    def __init__(self, broker, topic):
        #def settimeout(duration):
        #    pass
        self._queue = []
        self._broker = broker
        self._topic = topic
        self._client = MQTTClient("pytrack", self._broker, port=1883)
        self._busy = False
        #self._client.settimeout = settimeout
        self._client.connect()
        self._chrono = Timer.Chrono()
        self._chrono.start()
        print("Connected to MQTT broker %s"%self._broker)
        self._client.publish(self._topic, "Hello!")
        _thread.start_new_thread(self._loop, [.001]) # ever loop with small delay
        pass

    def push(self, message):
        self._queue.append(message)
        print('in <-', message)
        pass

    def pull(self):

        global inactivity_timer

        n = len(self._queue)
        if n > 0:
            self._busy = True
            #try:
            message = self._queue.pop(0)
            print('out->', message)
            self._client.publish(self._topic, message)
            #except MQTTException:
            #    print('MQTT Exception raised')
            self._chrono.reset()
            self._busy = False

    def _loop(self, delay):
        while True:
            if not self._busy:
                self.pull()
                time.sleep(delay)


    def get_timeout(self):
        return self._chrono.read()

#queue = MessageBuffer(broker="mqtt.avist.io", topic="/accelerometer")
