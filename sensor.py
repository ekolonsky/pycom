import time
import _thread
from machine import Pin
from onewire import DS18X20  # for temperature sensor
from onewire import OneWire  # for temperature sensor
from pytrack import Pytrack
from LIS2HH12 import LIS2HH12 # acelerometer
from L76GNSS import L76GNSS   # geolocation
from pytrack import Pytrack   # inactivity
from machine import Timer     # inactivity



class Sensor:

  def __init__(self, queue):
      self._queue = queue
      self._busy = False
      self.value = 0
      pass

  def read(self):
      pass

  def last(self):
      return self.value

  def _run(self):
      pass

  def printout(self, message):
      print(message)
      #self._queue.push(message)


class PeriodicSensor(Sensor):

  def __init__(self, queue, period):
      Sensor.__init__(self, queue)
      self._period = period
      _thread.start_new_thread(self._run, [.001]) # ever loop with small delay
      pass

  def _run(self, period):
        while True:
            if not self._busy:
                self._busy = True
                self.read()
                self._busy = False
                time.sleep(period)


BUTTON_PIN = 'P11'

class ButtonSensor(Sensor):

  def __init__(self, queue, pinstr=BUTTON_PIN):
      self.pin = Pin(pinstr, mode=Pin.IN, pull=Pin.PULL_UP)
      self.pin.callback(Pin.IRQ_FALLING, self._run)
      Sensor.__init__(self)
      pass

#def button_pressed(pin):
#    print('button pressed')

  def _run(self, pin):
      self.printout('Button pressed')
      #self.value = True


ACCEL_TRESHOLD = 2000 # shake deteted when acceleration is more than  0.001xG
ACCEL_DURATION = 200  # shake duration is more than 200ms

class ShakeSensor(Sensor ):

  def __init__(self, queue,
                     accel_treshold=ACCEL_TRESHOLD,
                     accel_duration=ACCEL_DURATION):

      Sensor.__init__(self, queue)
      self._acc = LIS2HH12()
      # enable the activity/inactivity interrupts
      # set the accelereation threshold to 2000mG (2G) and the min duration to 200ms
      self._acc.enable_activity_interrupt(accel_treshold, accel_duration ,handler=self._handler)

  def _handler(self, pin_o):
      if pin_o():
          msg = "Shake"
          self.printout(msg)



class TemperatureSensor(PeriodicSensor):

    def __init__(self, queue, period, pin):
        self._ow = OneWire(pin)
        self._temp = DS18X20(self._ow)
        self.value = 0
        PeriodicSensor.__init__(self, period)

    def read(self):
        self.value = self._temp.read_temp_async()
        time.sleep(1)
        self._temp.start_conversion()
        time.sleep(1)
        pass

class GeolocationSensor(PeriodicSensor):
    def __init__(self, period):
        self._gps = L76GNSS()
        self.value = (0, 0)  # latitude, longitude
        PeriodicSensor.__init__(self, period)

    def read(self):
        self.value = self._gps.coordinates()


WAIT_BEFORE_SLEEP = 300      # time in seconds to wait if nothing happens, then go to go to sleep
TIME_TO_SLEEP = 3600         # time to sleep in seconds, then wake up.

class InactivitySensor(PeriodicSensor):

    def __init__(self, queue, period,
                       wait_before_sleep=WAIT_BEFORE_SLEEP,
                       time_to_sleep=TIME_TO_SLEEP):

        self._wait_before_sleep = wait_before_sleep
        self._time_to_sleep = time_to_sleep
        self._queue = queue
        self._py = Pytrack()
        message = "Wake up reason: " + str(self._py.get_wake_reason())
        # display the reset reason code and the sleep remaining in seconds
        # possible values of wakeup reason are:
        # WAKE_REASON_ACCELEROMETER = 1
        # WAKE_REASON_PUSH_BUTTON = 2
        # WAKE_REASON_TIMER = 4
        # WAKE_REASON_INT_PIN = 8
        print(message)
        time.sleep(0.5)
        # enable wakeup source from INT pin
        self._py.setup_int_pin_wake_up(False)
        self._inactivity_timer = 0

    def read(self):
        self.value = self._queue.get_timeout()
        inactivity_time = self.value
        print('Inactivity timer acc:', inactivity_time)
        if inactivity_time > self._wait_before_sleep:
            print('Going to sleep for %ss'%self._time_to_sleep)
            #self._queue.push('Sleeping..')
            self._queue._chrono.reset()
            #self._py.setup_sleep(self._time_to_sleep)
            #time.sleep(1)
            #self._py.go_to_sleep()


#t = TemperatureSensor(period=5, pin=Pin('P12'))
#b = ButtonSensor(pinstr='P11')
#a = ShakeSensor()
#g = GeolocationSensor(period=5)

#while True:
#    print('T ', t.last())
#    print('G ', g.last())
#    time.sleep(5)
