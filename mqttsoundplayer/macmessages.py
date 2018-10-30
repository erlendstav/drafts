import pygame
import paho.mqtt.client as mqtt
import time

sound_loc = "/Users/erlendstav/Downloads/"
#sound_loc = "/home/pi/Downloads/"
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

def on_log(client, userdata, level, buf):
    print("log: ",buf)


#class MyMess():
#    topic = ""

pygame.init()
pygame.mixer.init()
laugh_sound = pygame.mixer.Sound(sound_loc + laugh_name)
howl_sound = pygame.mixer.Sound(sound_loc + howl_name)
#server_address="192.168.1.7"
#server_address="10.218.87.156"
server_address="localhost"
client = mqtt.Client("P1")
client.on_message=on_message
client.on_log=on_log
client.connect(server_address)
print("Starting...")
client.loop_start()
print("Started")
print("Publishing")
client.publish('test/topic', 'Hello from mac')
print("Published")
client.subscribe('halloween/toy01/#')
#client.publish("test/topic", 'Hello from pi')


#message = MyMess()
#message.topic = "halloween/toy1/laugh"
#on_playsound(message)
#time.sleep(10)
#message.topic = "halloween/toy1/howl"
#on_playsound(message)
#time.sleep(15)

time.sleep(30)
client.loop_stop()
