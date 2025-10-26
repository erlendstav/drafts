import pygame
import pygame._sdl2 as sdl2
import paho.mqtt.client as mqtt
from time import sleep
import os

#server_address = "192.168.0.100"
server_address="192.168.1.50"

# Sound
#SPEAKERS = 'Jabra SPEAK 510 USB'
#SPEAKERS = 'aFUNK'
#SPEAKERS = 'aMOVE'
#
#SPEAKERS = 'SRS-XB43'
# SPEAKERS = 'External Headphones'
# SPEAKERS = 'JBL Clip 2'

SOUND_LOC = os.getcwd() + "/"
FRIENDLY_MUSIC_NAME = "music_friendly.mp3"
SCARY_MUSIC_NAME = "music_scary.mp3"

TP_LOCATION = "garage"
TP_MUSIC = TP_LOCATION + "/music"

#SENSOR_TOPIC = "sensor/distance"
FRIENDLY_MUSIC_TOPIC = TP_MUSIC + "/friendly"
SCARY_MUSIC_TOPIC= TP_MUSIC + "/scary"
STOP_MUSIC_TOPIC= TP_MUSIC + "/stop"
SUBSCRIBE_TOPIC = TP_MUSIC + "/#"
CLIENT_NAME = "GarageMusicPlayer"


def play_friendly():
    pygame.mixer.stop()
    friendly_sound.play()


def play_scary():
    pygame.mixer.stop()
    scary_sound.play()


def stop_music():
    pygame.mixer.stop()


def on_play_friendly(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    play_friendly()


def on_play_scary(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    play_scary()


def on_stop_music(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    stop_music()


def on_message(client, userdata, message):
    print("topic : ", message.topic + " ignored")


pygame.mixer.init() #devicename=SPEAKERS)
print("Devices")
print(sdl2.audio.get_audio_device_names(False))
friendly_sound = pygame.mixer.Sound(SOUND_LOC + FRIENDLY_MUSIC_NAME)
scary_sound = pygame.mixer.Sound(SOUND_LOC + SCARY_MUSIC_NAME)

play_friendly()
sleep(3)
print("Played friendly music")
play_scary()
print("Played friendly music")
sleep(3)
stop_music()

client = mqtt.Client(client_id=CLIENT_NAME)
client.on_message=on_message
client.message_callback_add(SCARY_MUSIC_TOPIC, on_play_scary)
client.message_callback_add(FRIENDLY_MUSIC_TOPIC, on_play_friendly)
client.message_callback_add(STOP_MUSIC_TOPIC, on_stop_music)

client.connect(server_address)
client.loop_start()
client.subscribe(SUBSCRIBE_TOPIC)
client.publish("topic/state", "Hello from " + CLIENT_NAME)

while True:
    sleep(5)

client.loop_stop()
