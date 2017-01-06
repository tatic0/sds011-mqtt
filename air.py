import subprocess
import re
import sys
import time
import datetime
import paho.mqtt.client as paho



def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
# How long to wait (in seconds) between measurements.
client = paho.Client()
client.on_connect = on_connect
client.connect("your.mqtt.broker", 1883)
client.loop_start()


freq = 3600  # refresh 60 min


try:
# Continuously append data
  while True:
    output = subprocess.check_output(["od", "--endian=big" ,"-x", "-N10", "/dev/ttyUSB0"])
    data = output.split()[2:4]
    print(data)
    rawpm25 = (data[0][:2], data[0][2:4])
    rawpm10 = (data[1][:2], data[1][2:4])
    pm25 = str(int(rawpm25[1],16) * 256 + int(rawpm25[0], 16) / 10)
    pm10 = str(int(rawpm10[1],16) * 256 + int(rawpm10[0], 16) / 10)
    now = str(time.time())
    print(now,pm25,pm10)
    # Wait half an hour between each measurement
    (rc, mid) = client.publish("sensor/pm25", pm25, qos=1)
    (rc, mid) = client.publish("sensor/pm10", pm10, qos=1)
    time.sleep(freq)
except KeyboardInterrupt:
  print("You pressed ctrl-c, quitting")
  sys.exit(0)
