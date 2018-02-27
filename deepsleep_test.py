from pytrack import Pytrack
from LIS2HH12 import LIS2HH12
#from deepsleep import DeepSleep
import deepsleep

ACCEL_TRESHOLD = 2000 # shake deteted when acceleration is more than  0.001xG
ACCEL_DURATION = 200  # shake duration is more than 200ms

ds = deepsleep.DeepSleep()
py = Pytrack()
py.setup_int_wake_up(True, False)
acc = LIS2HH12()

def handler(pin_o):
  print('Acc handler event', pin_o())

acc.enable_activity_interrupt(ACCEL_TRESHOLD, ACCEL_DURATION, handler=handler)

# get the wake reason and the value of the pins during wake up
wake_s = ds.get_wake_status()
print(wake_s)

if wake_s['wake'] == deepsleep.PIN_WAKE:
    print("Pin wake up")
elif wake_s['wake'] == deepsleep.TIMER_WAKE:
    print("Timer wake up")
else:  # deepsleep.POWER_ON_WAKE:
    print("Power ON reset")

pins = ['P17', 'P18', 'P10']
ds.enable_pullups(pins)  # can also do ds.enable_pullups(['P17', 'P18'])
ds.enable_wake_on_fall(pins) # can also do ds.enable_wake_on_fall(['P17', 'P18'])
#ds.enable_wake_on_raise(pins) # can also do ds.enable_wake_on_fall(['P17', 'P18'])

ds.go_to_sleep(120)  # go to sleep for 60 seconds
