import pygame
import paho.mqtt.client as mqtt
import time

sound_loc = "/Users/erlendstav/Halloween/Sounds/"

dog_bark_sound = ""
dog_growl_sound = ""
victim_helpme_sound = ""
victim_helphelp_sound = ""

dog_bark_name = "dog_bark.wav"
dog_growl_name = "dog_snarl.wav"
victim_helpme_name = "helpme.wav"
victim_helphelp_name = "helphelp.wav"


def on_playsound(message):
    if message.topic.endswith("dog/bark"):
        dog_bark_sound.play()
    elif message.topic.endswith("dog/growl"):
        dog_growl_sound.play()
    elif message.topic.endswith("victim/helpme"):
        victim_helpme_sound.play()
    elif message.topic.endswith("scarface/helphelp"):
        victim_helphelp_sound.play()
    else:
        return

def on_message(client, userdata, message):
    print("topic : ", message.topic)
    on_playsound(message)

def on_log(client, userdata, level, buf):
    print("log: ",buf)

pygame.init()
pygame.mixer.init()

print("Bark...")
dog_bark_sound = pygame.mixer.Sound(sound_loc + dog_bark_name)
time.sleep(2)
print("Growl...")
dog_growl_sound = pygame.mixer.Sound(sound_loc + dog_growl_name)
print("Helpme...")
victim_helpme_sound = pygame.mixer.Sound(sound_loc + victim_helpme_name)
print("Helphelp...")
victim_helphelp_sound = pygame.mixer.Sound(sound_loc + victim_helphelp_name)
print("Sounds loaded")

#server_address="192.168.1.7"
#server_address="10.218.87.156"
server_address="localhost"
print("Createing mqtt client...")

client = mqtt.Client("iMacSmall")
print("On mess")
client.on_message=on_message
print("On log")
client.on_log=on_log
print("Connecting...")
client.connect(server_address)
print("Starting...")
client.loop_start()
print("Started")
print("Publishing")
client.publish('test/topic', 'Hello from small iMac')
print("Published")
client.subscribe('halloween/dog/#')
client.subscribe('halloween/victim/#')

while True:
    time.sleep(5)

client.loop_stop()
