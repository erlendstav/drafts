import paho.mqtt.client as mqtt
import time


server_address="localhost"

def on_message(client, userdata, message):
    print("topic : ", message.topic)

def on_log(client, userdata, level, buf):
    print("log: ",buf)


print("Creating client...")
client = mqtt.Client("Scenario")
print("On mess")
client.on_message=on_message
print("On log")
client.on_log=on_log
print("Connect")
client.connect(server_address)
print("Starting...")
client.loop_start()
print("Started")

while True:
    client.publish('halloween/victim/helpme', '1')
    time.sleep(3)
    client.publish('halloween/light/start', '3')
    time.sleep(4)
    publishing('halloween/scarface/laugh', '2')
    time.sleep(2)
    client.publish('halloween/dog/bark', '4')
    time.sleep(2)
    client.publish('halloween/baby/laugh', '5')
    time.sleep(3)
    client.publish('halloween/redhead/eat', '6')
    time.sleep(5)
    client.publish('halloween/dog/bark', '7')
    time.sleep(3)
    client.publish('halloween/victim/helphelp', '8')
    time.sleep(2)
    client.publish('halloween/scarface/nomercy', '9')
    time.sleep(5)
    client.publish('halloween/dog/growl', '10')
    time.sleep(1)
    client.publish('halloween/victim/helphelp', '11')
    time.sleep(2)
    client.publish('halloween/baby/cry', '12')
    time.sleep(2)
    client.publish('halloween/scarface/laugh', '13')
    time.sleep(15)

client.loop_stop()
