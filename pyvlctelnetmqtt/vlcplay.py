import paho.mqtt.client as mqtt
from python_telnet_vlc import VLCTelnet
import time

print("A")
v = VLCTelnet("192.168.1.10", "admin", 4212)
print("A")
v.clear()
v.add("/Users/erlendstav/Movies/Halloween/Halloween2020/PHA_Spinster_BehaveOrBeDead_Win_H.mp4")
v.add("/Users/erlendstav/Movies/Halloween/Halloween2020/Diabolic Debutant_Dancing Queen_Win_H.mp4")
v.add("/Users/erlendstav/Movies/Halloween/Halloween2020/silly.mp4")
print("A")
#v.fullscreen()
#print("A")
v.play()
print("A")
while True:
    time.sleep(5)
    print("A")
