import paho.mqtt.client as mqtt
import time

server_address="192.168.1.50"
#server_address="localhost"
#sound_loc = "/Users/erlend/Halloween/Sounds/"

#eat_sound = ""
#eat_name = "eating.wav"
#howl_name = "wlaugh.wav"


def on_playvideo(message):
    if message.topic.endswith("scare"):
        print("Starting video " + message.topic)
#    else:
#        print("Message received " + message.topic)

def on_message(client, userdata, message):
    print("topic : ", message.topic)
    on_playvideo(message)
    
client = mqtt.Client("ErlendsNewMacBookPro")
#print("Client")
client.on_message=on_message
#print("Client")
client.connect(server_address)
#print("Client")
client.loop_start()
#print("Client")
client.subscribe("alle/#")
print("Sub1")
client.subscribe("soverom/#")
#print("Client")
client.publish("test/state", "Hello from Python")

while True:
    time.sleep(5)

client.loop_stop()