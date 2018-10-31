import os
import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("mr: " , str(message.payload.decode("utf-8")))
    print("topic : ", message.topic)
    if message.topic.endswith("start"):
        cmd = """
        osascript -e 'tell application "Lightkey"' -e 'activate' -e 'tell application "System events" to key code 113' -e 'end tell'
        """
        # minimize active window
        os.system(cmd)

def on_log(client, userdata, level, buf):
    print("log: ",buf)


#server_address="192.168.1.7"
#server_address="10.218.87.156"
server_address="localhost"
client = mqtt.Client("Lights")
client.on_message=on_message
client.on_log=on_log
client.connect(server_address)
print("Starting...")
client.loop_start()
print("Started")
print("Publishing")
client.publish('test/topic', 'Hello from lights')
print("Published")
client.subscribe('halloween/lights/#')
client.publish("test/topic", 'Hello from lights')


while True:
    time.sleep(5)

client.loop_stop()
