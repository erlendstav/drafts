import pygame
import pygame._sdl2 as sdl2
import paho.mqtt.client as mqtt
from time import sleep
import os

server_address = "192.168.0.100"

# Sound
#SPEAKERS = 'Jabra SPEAK 510 USB'
#SPEAKERS = 'aFUNK'
#SPEAKERS = 'aMOVE'
#
SPEAKERS = 'SRS-XB43'
# SPEAKERS = 'External Headphones'
# SPEAKERS = 'JBL Clip 2'

SOUND_LOC = os.getcwd() + "/"
TWINKLE1_SOUND_NAME = "Twinkle1.mp3"
TWINKLE2_SOUND_NAME = "Twinkle2.mp3"
ROCKABY_SOUND_NAME = "Rockaby.mp3"
ROWROW_SOUND_NAME = "Rowrow.mp3"

WAKEUP_SOUND_NAME = "SmokeIntro.mp3"

TP_LOCATION = "garage"
TP_MUSIC = TP_LOCATION + "/music"

#SENSOR_TOPIC = "sensor/distance"
LULLABY_TOPIC = TP_MUSIC + "/lullaby"
WAKEUP_TOPIC = TP_MUSIC + "/wakeup"
SUBSCRIBE_TOPIC = TP_MUSIC + "/#"
CLIENT_NAME = "GarageMusicPlayer"


def play_twinkle1():
    twinkle1_sound.play()


def play_twinkle2():
    twinkle2_sound.play()


def play_rockaby():
    rockaby_sound.play()


def play_rowrow():
    rowrow_sound.play()


def play_wakeup():
    pygame.mixer.stop()
    wakeup_sound.play()


def on_lullaby(mosq, obj, msg):
    #print("MESSAGES: " + msg.topic)
    global cr_lullaby
    pygame.mixer.stop()
    lullaby_list[cr_lullaby].play()
    cr_lullaby = cr_lullaby+1
    if cr_lullaby == len(lullaby_list):
        cr_lullaby = 0


def on_wakeup(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    play_wakeup()


def on_message(client, userdata, message):
    print("topic : ", message.topic + " ignored")


pygame.mixer.init(devicename=SPEAKERS)
print("Devices")
print(sdl2.audio.get_audio_device_names(False))
twinkle1_sound = pygame.mixer.Sound(SOUND_LOC + TWINKLE1_SOUND_NAME)
twinkle2_sound = pygame.mixer.Sound(SOUND_LOC + TWINKLE2_SOUND_NAME)
rockaby_sound = pygame.mixer.Sound(SOUND_LOC + ROCKABY_SOUND_NAME)
rowrow_sound = pygame.mixer.Sound(SOUND_LOC + ROWROW_SOUND_NAME)
lullaby_list = [twinkle1_sound, rowrow_sound, twinkle2_sound, rockaby_sound]
cr_lullaby = 0
wakeup_sound = pygame.mixer.Sound(SOUND_LOC + WAKEUP_SOUND_NAME)

#on_lullaby(" ", " ", " ")
#sleep(7)
#on_lullaby(" ", " ", " ")
#sleep(7)
#on_lullaby(" ", " ", " ")
#sleep(7)
#on_lullaby(" ", " ", " ")
#sleep(7)
on_lullaby(" ", " ", " ")
sleep(7)
print("Played lullaby sounds")
play_wakeup()
sleep(7)
#print("Played wakeup sound")

client = mqtt.Client(CLIENT_NAME)
client.on_message=on_message
client.message_callback_add(LULLABY_TOPIC, on_lullaby)
client.message_callback_add(WAKEUP_TOPIC, on_wakeup)

client.connect(server_address)
client.loop_start()
client.subscribe(SUBSCRIBE_TOPIC)
client.publish("topic/state", "Hello from " + CLIENT_NAME)

while True:
    sleep(5)

client.loop_stop()
