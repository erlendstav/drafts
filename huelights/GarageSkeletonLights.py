import random

import paho.mqtt.client as mqtt
from phue import Bridge
from time import sleep


HUE_Original = 8417
HUE_Plain = 9277
HUE_Green = 18801
HUE_Red = 273
HUE_PurpleBlue = 48671
HUE_PINK = 48671
HUE_Blue = 44963
HUE_WARM_ORANGE = 7207

# Rooms / groups

ROOM_GARAGE = "Garasje"
ROOM_GARAGE_OTHER = "GarasjeAndre"

# Scenes
SCENE_FRIENDLY_START = "Friendly"
SCENE_SPELLBOUND = "Spellbound"

SCENE_SCARY_START = "Start"
SCENE_CLOSET = "Skap"
SCENE_CATS = "Katter"
SCENE_START_AND_RECEPTION = "Start og resepsjon"

SKELETON_LIGHT_NAME = "Lightbulb1"
CAT_LIGHT_NAME = "Hue Play 1"
CLOSET_LIGHT_NAME = "Hue Play 2"
RECEPTION_LIGHT_NAME = "Lightbulb2"
CEILING_LIGHT_NAME = "Lightbulb3"
SPOT_LIGHT_NAME = "Colorspot1"

CAT_LIGHT_ID = 4
CLOSET_LIGHT_ID = 6

def highlight(light_id, hue):
    return

def flicker(lightname, max_bri, times):
    org_bri = light_named[lightname].brightness
    min_flicker = org_bri + round((max_bri-org_bri) / 3)
    for t in range(times):
        light_named[lightname].brightness = random.randrange(min_flicker, max_bri)
        sleep(0.8)
        light_named[lightname].brightness = org_bri
        sleep(random.randrange(1, 3))

def on_message(client, userdata, message):
    print("topic : ", message.topic)
    if message.topic.endswith("cat.lightup"):
        highlight(CAT_LIGHT_ID, HUE_WARM_ORANGE)
    elif message.topic.endswith("closet.highlight"):
        highlight(CLOSET_LIGHT_ID, HUE_Red)
        #howl_sound.play()
        #sound_name = "laughhowl1.mp3"
    else:
        return


"""
client = mqtt.Client("GarageLightController")
client.on_message=on_message
client.connect(server_address)
client.loop_start()
client.subscribe("garage/lights/#")
client.publish("topic/state", "Hello from GarageLightController")
"""

b = Bridge('192.168.1.21')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# b.get_api()

lights = b.lights
light_named = b.get_light_objects('name')

for l in lights:
    print(l.name, l.light_id)

print("Switch :", light_named["Hue smart plug 1"].on)

print("Play 1 :", light_named["Hue Play 1"].on, light_named["Hue Play 1"].hue, light_named["Hue Play 1"].brightness)
print("Play 2 :", light_named["Hue Play 2"].on, light_named["Hue Play 2"].hue)

#light_named["Hue Play 1"].hue = HUE_WARM_ORANGE
sleep(2)

b.run_scene(ROOM_GARAGE, SCENE_SCARY_START)
print("Start")
flicker(SKELETON_LIGHT_NAME, 100, 5)
sleep(5)
b.run_scene(ROOM_GARAGE, SCENE_CLOSET)
flicker(CLOSET_LIGHT_NAME, 250, 5)
print("Closet")
sleep(5)
b.run_scene(ROOM_GARAGE, SCENE_CATS)
print("Cats")
sleep(5)
b.run_scene(ROOM_GARAGE, SCENE_SCARY_START)
print("Start")


#command =  {'transitiontime' : 50, 'bri' : 200, 'hue' : Hue_Red}
#b.set_light(4, command)
#sleep(6)

#command =  {'transitiontime' : 100, 'bri' : 50, 'hue' : Hue_Green}
#b.set_light(4, command)
#b.set_light(6, command)
#sleep(12)

"""
light_named["Hue Play 1"].transitiontime = 3
light_named["Hue Play 1"].brightness = 100
sleep(2)
light_named["Hue Play 1"].hue = Hue_WarmOrange

sleep(2)
light_named["Hue Play 1"].brightness = 50
sleep(3)
light_named["Hue Play 1"].brightness = 150
sleep(0.5)
light_named["Hue Play 1"].brightness = 50
sleep(3)
light_named["Hue Play 1"].brightness = 200
sleep(0.5)
light_named["Hue Play 1"].brightness = 100
sleep(0.5)
light_named["Hue Play 1"].transitiontime = 1
light_named["Hue Play 1"].on = False
sleep(3)
light_named["Hue Play 1"].on = True
sleep(0.3)
light_named["Hue Play 1"].on = False
sleep(2)
light_named["Hue Play 1"].on = True
sleep(0.2)
light_named["Hue Play 1"].brightness = 170
sleep(0.3)
light_named["Hue Play 1"].brightness = 50
sleep(0.5)
light_named["Hue Play 1"].on = False
sleep(2)
light_named["Hue Play 1"].on = True
sleep(2)


"""
#lights["Hue smart plug 1"].on = True
#sleep(5)
#lights["Hue smart plug 1"].on = False

#for l in lights:
#    print(l.name)
