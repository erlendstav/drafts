import pygame
import pygame._sdl2 as sdl2
import paho.mqtt.client as mqtt
from time import sleep
import os

server_address = "192.168.0.100"

# Sound
#SPEAKERS = 'Jabra SPEAK 510 USB'
SPEAKERS = 'aFUNK'
# SPEAKERS = 'aMOVE'
# SPEAKERS = 'JBL Clip 2'

SOUND_LOC = os.getcwd() + "/"
OK_SOUND_NAME = "spider_ok.mp3"
WAKEUP_SOUND_NAME = "spider_wake.mp3"

#SENSOR_TOPIC = "sensor/distance"

#OK_TOPIC = "spider/sound/ok"
#WAKEUP_TOPIC = "spider/sound/wakeup"
OK_TOPIC = "garage/acceleration/triggered"
SUBSCRIBE_TOPIC = OK_TOPIC # "spider/#"
CLIENT_NAME = "SpiderSoundPlayer"


def play_ok():
    ok_sound.play()


#def play_wakeup():
#    wakeup_sound.play()


def on_status_ok(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    play_ok()


#def on_wakeup(mosq, obj, msg):
#    print("MESSAGES: " + msg.topic)
#    play_wakeup()


def on_message(client, userdata, message):
    print("topic : ", message.topic + " ignored")


#pygame.mixer.init()
pygame.mixer.init(devicename=SPEAKERS)
print("Devices")
print(sdl2.audio.get_audio_device_names(False))
ok_sound = pygame.mixer.Sound(SOUND_LOC + WAKEUP_SOUND_NAME)
#ok_sound = pygame.mixer.Sound(SOUND_LOC + OK_SOUND_NAME)
#wakeup_sound = pygame.mixer.Sound(SOUND_LOC + WAKEUP_SOUND_NAME)
play_ok()
sleep(7)
print("Played ok sound")
#play_wakeup()
#sleep(7)
#print("Played wakeup sound")

client = mqtt.Client(CLIENT_NAME)
client.on_message=on_message
client.message_callback_add(OK_TOPIC, on_status_ok)
#client.message_callback_add(WAKEUP_TOPIC, on_wakeup)

client.connect(server_address)
client.loop_start()
client.subscribe(SUBSCRIBE_TOPIC)
client.publish("topic/state", "Hello from " + CLIENT_NAME)

while True:
    sleep(5)

client.loop_stop()
