import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P12
ow = OneWire(Pin('P12'))
temp = DS18X20(ow)

while True:
    print(temp.read_temp_async())
    time.sleep(1)
    temp.start_conversion()
    time.sleep(1)
