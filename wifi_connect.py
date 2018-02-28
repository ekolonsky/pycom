from network import WLAN
import machine

SSID = "itps-guest" #"Wart-29"
PASS = "parmafree"  # "77599544151"

print("Connecting to WiFi %s.."%SSID)
wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)
wlan.connect(SSID, auth=(WLAN.WPA2, PASS), timeout=5000)
while not wlan.isconnected():
     machine.idle()
print("Connected to Wifi %s"%SSID)
