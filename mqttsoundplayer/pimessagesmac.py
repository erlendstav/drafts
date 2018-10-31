import pygame
import paho.mqtt.client as mqtt
import time

#server_address="192.168.1.7"
server_address="localhost"
sound_loc = "/Users/erlend/Halloween/Sounds/"
#sound_loc = "/Users/erlendstav/Halloween/Sounds/"

eat_sound = ""
#howl_sound = ""
eat_name = "eating.wav"
#howl_name = "wlaugh.wav"


def on_playsound(message):
    if message.topic.endswith("eat"):
        eat_sound.play()
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
eat_sound = pygame.mixer.Sound(sound_loc + eat_name)
#howl_sound = pygame.mixer.Sound(sound_loc + howl_name)

client = mqtt.Client("PiZero")
client.on_message=on_message
client.connect(server_address)
client.loop_start()
client.subscribe("halloween/redhead/#")
client.publish("topic/state", "Hello from Pi Zero")

while True:
    time.sleep(5)

client.loop_stop()