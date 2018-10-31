import pygame
import paho.mqtt.client as mqtt
import time

sound_loc = "/Users/erlendstav/Documents/Private/Halloween/"
baby_laugh_sound = ""
baby_cry_sound = ""
scarface_laugh_sound = ""
scarface_no_mercy_sound = ""

baby_laugh_name = "baby_laugh_short.wav"
baby_cry_name = "baby_cry.wav"
scarface_laugh_name = "deeplaugh.mp3"
scarface_no_mercy_name = "scarface_no_mercy.wav"


def on_playsound(message):
    if message.topic.endswith("baby/laugh"):
        baby_laugh_sound.play()
    elif message.topic.endswith("baby/cry"):
        baby_cry_sound.play()
    elif message.topic.endswith("scarface/laugh"):
        scarface_laugh_sound.play()
    elif message.topic.endswith("scarface/nomercy"):
        scarface_no_mercy_sound.play()
    else:
        return

def on_message(client, userdata, message):
    print("topic : ", message.topic)
    on_playsound(message)

def on_log(client, userdata, level, buf):
    print("log: ",buf)

pygame.init()
pygame.mixer.init()

print("Client...")
baby_laugh_sound = pygame.mixer.Sound(sound_loc + baby_laugh_name)
#baby_laugh_sound = pygame.mixer.Sound("/Users/erlendstav/Documents/Private/Halloween/baby_laugh_short.wav")
time.sleep(2)
print("Client...")
baby_cry_sound = pygame.mixer.Sound(sound_loc + baby_cry_name)
print("Client...")
scarface_laugh_sound = pygame.mixer.Sound(sound_loc + scarface_no_mercy_name)
print("Client...")
scarface_no_mercy_sound = pygame.mixer.Sound(sound_loc + scarface_no_mercy_name)
print("Client...")

#server_address="192.168.1.7"
#server_address="10.218.87.156"
server_address="localhost"
print("Client...")

client = mqtt.Client("MBPro")
print("On mess")
client.on_message=on_message
print("On log")
client.on_log=on_log
print("Connect")
client.connect(server_address)
print("Starting...")
client.loop_start()
print("Started")
print("Publishing")
client.publish('test/topic', 'Hello from mac book pro')
print("Published")
client.subscribe('halloween/baby/#')
client.subscribe('halloween/scarface/#')

while True:
    time.sleep(5)

client.loop_stop()
