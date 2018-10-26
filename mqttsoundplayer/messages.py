import pygame
import paho.mqtt.client as mqtt
import time

def on_playsound():
    pygame.mixer.music.load("/home/pi/Downloads/cackle3.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy()== True:
        continue

def on_message(client, userdata, message):
    print("mr: " , str(message.payload.decode("utf-8")))
    print("topic : ", message.topic)

#pygame.mixer.init()
server_address="192.168.1.7"
client = mqtt.Client("P1")
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
client.subscribe("halloween/toy01/laugh")
client.publish("topic/state", "Hello from pi")
time.sleep(60)
client.loop_stop()
