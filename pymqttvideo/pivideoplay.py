import paho.mqtt.client as mqtt
import time
import random

server_address="192.168.1.50"
client_name = "Pi4Video1"

# scare levels
LVL_FRIENDLY = "level/friendly"
LVL_NORMAL = "level/normal"
LVL_SCARY = "level/scary"

# videos for levels

videos = {
    LVL_FRIENDLY : ["boo_scare_1.mp4", "boo_scare_2.mp4"],
    LVL_NORMAL : ["spinster_tea_1.mp4", "spinster_tea_2.mp4"],
    LVL_SCARY : ["Twisted Twins_Startle Scare1_Holl_H.mp4", "Diabolic Debutant_Startle Scare_Win_H.mp4"]
}

scare_level = lvl_friendly

def play_video(video_name):
    print("Playing video " + video_name)

def play_video_from_level(level):
    candidates = videos[level]
    print("Playing video from level " + level)    
    play_video(random.choice(candidates))


def on_message(client, userdata, message):
    if message.topic.endswith("movement1"):
        print("Movement detected: starting video " + message.topic)
        play_video_from_level(scare_level)
    elif message.topic.endswith(LVL_FRIENDLY):
        scare_level = LVL_FRIENDLY
        print("Scare level set to " + lvl_friendly)
    elif message.topic.endswith(LVL_NORMAL):
        scare_level = LVL_NORMAL
        print("Scare level set to " + LVL_NORMAL)
    elif message.topic.endswith(LVL_SCARY):
        scare_level = LVL_SCARY
        print("Scare level set to " + LVL_SCARY)
    else:
        print("Unknown message " + message.topic)
        return

def setup_mqtt():
    client = mqtt.Client(clien_name)
    client.on_message=on_message
    client.connect(server_address)
    client.loop_start()
    return client

client = setup_mqtt()
client.subscribe("garage/#")
client.publish("test/hello", "Hello from " + clientName)

while True:
    time.sleep(5)
    client.publish("status/alive/" + clientName)

client.loop_stop()