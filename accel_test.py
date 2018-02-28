from LIS2HH12 import LIS2HH12

def handler(pin_o):
  if pin_o():
      a = acc.acceleration() # tuple (ax, ay, az)
      g = (a[0]*a[0] + a[1]*a[1] + a[2]*a[2])**0.5 # abs(a)
      msg = "shake level %f"%g
      print(msg)

acc = LIS2HH12()
# enable the activity/inactivity interrupts
# set the accelereation threshold to 2000mG (2G) and the min duration to 200ms


acc.enable_activity_interrupt(2000, 200 ,handler=handler)
#acc._user_handler = handler

print('Shake me.')
