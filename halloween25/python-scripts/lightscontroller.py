import pygame
import pygame._sdl2 as sdl2
import paho.mqtt.client as mqtt
from time import sleep
import os
from pythonosc.udp_client import SimpleUDPClient

#server_address = "192.168.0.100"
server_address="192.168.1.50"


# MQTT Topics
TOPIC_LOCATION = "garage"
TOPIC_LIGHT = TOPIC_LOCATION + "/light"

# Scare levels
LVL_FRIENDLY = "friendly"
#LVL_NORMAL = "normal"
LVL_SCARY = "scary"

# MQTT Topics listened to
TOPIC_LIGHT_START_FRIENDLY = TOPIC_LIGHT + "/start/" + LVL_FRIENDLY
TOPIC_LIGHT_START_SCARY = TOPIC_LIGHT + "/start/" + LVL_SCARY
TOPIC_LIGHT_SUMMON_FRIENDLY = TOPIC_LIGHT + "/summon/" + LVL_FRIENDLY
TOPIC_LIGHT_SUMMON_SCARY = TOPIC_LIGHT + "/summon/" + LVL_SCARY
TOPIC_LIGHT_DARK = TOPIC_LIGHT + "/dark"
TOPIC_LIGHT_EXIT = TOPIC_LIGHT + "/exit"

#SENSOR_TOPIC = "sensor/distance"
SUBSCRIBE_TOPIC = TOPIC_LIGHT + "/#"
CLIENT_NAME = "GarageLightController"


def on_light_start_friendly(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/PartyFriendly/start", "")


def on_light_start_scary(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/PartyScary/start", "")


def on_light_summon_friendly(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/SummonFriendly/start", "")


def on_light_summon_scary(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/SummonScary/start", "")


def on_light_dark(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/Dark/start", "")


def on_light_exit(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/PartyDone/start", "")


def on_message(client, userdata, message):
    print("topic : ", message.topic + " ignored")


# init osc client
ip = "localhost"
port = 21600
client = SimpleUDPClient(ip, port)  # Create client

# Set up MQTT client and subscriptions
mclient = mqtt.Client(client_id=CLIENT_NAME)
mclient.on_message=on_message
mclient.message_callback_add(TOPIC_LIGHT_START_FRIENDLY, on_light_start_friendly)
mclient.message_callback_add(TOPIC_LIGHT_START_SCARY, on_light_start_scary)
mclient.message_callback_add(TOPIC_LIGHT_SUMMON_FRIENDLY, on_light_summon_friendly)
mclient.message_callback_add(TOPIC_LIGHT_SUMMON_SCARY, on_light_summon_scary)
mclient.message_callback_add(TOPIC_LIGHT_DARK, on_light_dark)
mclient.message_callback_add(TOPIC_LIGHT_EXIT, on_light_exit)

mclient.connect(server_address)
mclient.loop_start()
mclient.subscribe(SUBSCRIBE_TOPIC)
mclient.publish("topic/state", "Hello from " + CLIENT_NAME)

while True:
    sleep(5)

mclient.loop_stop()
