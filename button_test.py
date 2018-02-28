from machine import Pin
import time


def button_pressed(pin):
    print('button pressed')

print('Press button..')

pin = Pin('P11', mode=Pin.IN, pull=Pin.PULL_UP)
pin.callback(Pin.IRQ_FALLING, button_pressed)
