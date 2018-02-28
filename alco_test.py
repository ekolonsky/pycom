from machine import ADC
import time

adc = ADC()
#adc.vref_to_pin('P22')

adc_c = adc.channel(pin='P20')


adc_c()

while True:
    print(adc_c.value())
    time.sleep(1)
