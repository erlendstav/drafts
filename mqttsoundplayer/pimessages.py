import pygame
import paho.mqtt.client as mqtt
import time

sound_loc = "/home/pi/Halloween/Sounds"
eat_sound = ""
#howl_sound = ""
eat_name = "eating.wav"
#howl_name = "wlaugh.wav"


def on_playsound(message):
    if message.topic.endswith("eat"):
        laugh_sound.play()
        #sound_name = "cackle3.mp3"
    #elif message.topic.endswith("howl"):
        #howl_sound.play()
        #sound_name = "laughhowl1.mp3"
    else:
        return

def on_message(client, userdata, message):
    print("topic : ", message.topic)
    on_playsound(message)
    
pygame.mixer.init()
laugh_sound = pygame.mixer.Sound(sound_loc + laugh_name)
howl_sound = pygame.mixer.Sound(sound_loc + howl_name)
#server_address="192.168.1.7"
server_address="localhost"
client = mqtt.Client("PiZero")
client.on_message=on_message
client.connect(server_address)
client.loop_start()
client.subscribe("halloween/redhead/#")
client.publish("topic/state", "Hello from Pi Zero")

while True:
    time.sleep(5)

client.loop_stop()