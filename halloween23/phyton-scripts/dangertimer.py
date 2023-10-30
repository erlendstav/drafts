import paho.mqtt.client as mqtt
from time import sleep

server_address = "192.168.0.100"

TP_LOCATION = "garage"

#SENSOR_TOPIC = "sensor/distance"
CLIENT_NAME = "GarageDangerTimer"

CONTROLLER_START_TOPIC = TP_LOCATION + "/controller/start"
RED_BUTTON_TOPIC = TP_LOCATION + "/redbutton/pressed"
TOPIC_DANGER_TIMER = TP_LOCATION + "/dangertimer"



def on_controller_start(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    global initial_countdown
    global timer_active
    initial_countdown= MAX_COUNTDOWN
    timer_active = True


def on_red_button_triggered(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    global timer_active
    timer_active = False


def on_message(client, userdata, message):
    print("topic : ", message.topic + " ignored")


MAX_COUNTDOWN = 6

timer_active = False
initial_countdown = MAX_COUNTDOWN

client = mqtt.Client(CLIENT_NAME)
client.on_message=on_message
client.message_callback_add(CONTROLLER_START_TOPIC, on_controller_start)
client.message_callback_add(RED_BUTTON_TOPIC, on_red_button_triggered)

client.connect(server_address)
client.loop_start()
client.subscribe(CONTROLLER_START_TOPIC)
client.subscribe(RED_BUTTON_TOPIC)
client.publish("topic/state", "Hello from " + CLIENT_NAME)

while True:
    sleep(5)
    if timer_active:
        if initial_countdown == 0:
            client.publish(TOPIC_DANGER_TIMER, "hi")
        else:
            initial_countdown = initial_countdown - 1

client.loop_stop()
