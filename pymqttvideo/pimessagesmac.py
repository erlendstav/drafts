import paho.mqtt.client as mqtt
import time

server_address="10.0.0.2"
#server_address="localhost"
#sound_loc = "/Users/erlend/Halloween/Sounds/"

eat_sound = ""
eat_name = "eating.wav"
#howl_name = "wlaugh.wav"


def on_playvideo(message):
    if message.topic.endswith("scare"):
        print("Starting video " + message.topic)
    else:
        return

def on_message(client, userdata, message):
    print("topic : ", message.topic)
    on_playvideo(message)
    
client = mqtt.Client("ErlendsMac")
client.on_message=on_message
client.connect(server_address)
client.loop_start()
client.subscribe("test/garage/#")
client.publish("test/state", "Hello from Python")

while True:
    time.sleep(5)

client.loop_stop()