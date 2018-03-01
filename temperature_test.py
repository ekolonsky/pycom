import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire


PIN_TEMP = Pin('P12')

class TemperatureSensor:

    def __init__(self, pin=PIN_TEMP):
        self._ow = OneWire(pin)
        self._temp = DS18X20(self._ow)
        self.temperature = 0
        pass

    def read(self):
        self.temperature = self._temp.read_temp_async()
        time.sleep(1)
        self._temp.start_conversion()
        time.sleep(1)
        pass

    def last(self):
        self.read()
        return self.temperature



t = TemperatureSensor()
while True:
    print(t.last())
