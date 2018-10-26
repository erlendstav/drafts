import pygame
import paho.mqtt.client as mqtt
import time

sound_loc = "/home/pi/Downloads/"
laugh_sound = ""
howl_sound = ""
#laugh_name = "cackle3.mp3"
laugh_name = "cackle3.wav"
howl_name = "wlaugh.wav"


def on_playsound(message):
    #sound_loc = "/home/pi/Downloads/"
    #sound_name = "";
    if message.topic.endswith("laugh"):
        laugh_sound.play()
        #sound_name = "cackle3.mp3"
    elif message.topic.endswith("howl"):
        howl_sound.play()
        #sound_name = "laughhowl1.mp3"
    else:
        return
    
    #pygame.mixer.music.load(sound_loc + sound_name)
    #pygame.mixer.music.load("/home/pi/Downloads/cackle3.mp3")
    #pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy()== True:
    #    continue

def on_message(client, userdata, message):
    print("mr: " , str(message.payload.decode("utf-8")))
    print("topic : ", message.topic)
    on_playsound(message)
    
pygame.mixer.init()
laugh_sound = pygame.mixer.Sound(sound_loc + laugh_name)
howl_sound = pygame.mixer.Sound(sound_loc + howl_name)
server_address="192.168.1.7"
client = mqtt.Client("P1")
client.on_message=on_message
client.connect(server_address)
client.loop_start()
client.subscribe("halloween/toy01/#")
client.publish("topic/state", "Hello from pi")
time.sleep(300)
client.loop_stop()
