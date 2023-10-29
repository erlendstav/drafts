import paho.mqtt.client as mqtt
from struct import *
from time import sleep
import os
import json
from enum import Enum
import threading

#server_address = "192.168.0.100"
server_address = "localhost"

SENSOR_PREFIX = "sensor/"

DEFAULT_LUL_EFFECT = 25

class GameState:
    def __init__(self, danger_level, lul_effect, is_waking_up):
        self.danger_level = danger_level
        self.lul_effect = lul_effect
        self.is_waking_up = is_waking_up

    def reset(self):
        self.danger_level = 0
        self.lul_effect = DEFAULT_LUL_EFFECT
        self.is_waking_up = False
        print("Game state reset")


game = GameState(0, DEFAULT_LUL_EFFECT, False)


NO_ARG = "hi"

DISTANCE_LOW = 60
DISTANCE_HIGH = 1000
DISTANCE_PAUSE = 15

ACCELERATION_LOW = 0.1
ACCELERATION_HIGH = 0.99
ACCELERATION_PAUSE = 15

LIGHT_LOW = 200
LIGHT_HIGH = 400
LIGHT_PAUSE = 15

MOTION_PAUSE = 15

DANGER_MEDIUM_THRESHOLD = 60
DANGER_HIGH_THRESHOLD = 98

PAUSE_FOR_WHITE_BUTTON_REENABLE = 5
PAUSE_BETWEEN_WAKEUP_MUSIC_AND_VIDEO = 10
PAUSE_BETWEEN_WAKEUP_MUSIC_AND_SMOKE = 15
PAUSE_FROM_START_OF_WAKEUP_TO_RESTART = 30

# Subtopics and topic prefix
ST_PRESSED = "pressed"
ST_TRIGGERED = "triggered"
ST_ENABLE = "enable"
ST_DISABLE = "disable"
ST_RANGE_LOW = "range/low" # 0-1000
ST_RANGE_HIGH = "range/high" # 0-1000
ST_TRIGGER_PAUSE = "pause" # 0-100 (sec)


ST_DANGER_LEVEL = "dangerlevel" # 0-100

TP_LOCATION = "garage"
TP_WHITE_BUTTON = TP_LOCATION + "/whitebutton"
TP_RED_BUTTON = TP_LOCATION + "/redbutton"
TP_DRAGON = "dragon"
TP_MUSIC = TP_LOCATION + "/music"

TP_DISTANCE = TP_LOCATION + "/distance"
TP_MOTION = TP_LOCATION + "/motion"
TP_LIGHT = TP_LOCATION + "/light"
TP_ACCELERATION = TP_LOCATION + "/acceleration"

#  Incomming topics and topic patterns
TOPIC_CONTROLLER_START = TP_LOCATION + "/controller/start"
PATTERN_TRIGGERED = TP_LOCATION + "/+/" + ST_TRIGGERED
TOPIC_WHITE_BUTTON_PRESSED = TP_WHITE_BUTTON + "/" + ST_PRESSED
TOPIC_RED_BUTTON_PRESSED = TP_RED_BUTTON + "/" + ST_PRESSED
#TOPIC_RED_BUTTON_TRIGGERED = "garage/redbutton/triggered"
#TOPIC_DISTANCE_TRIGGERED = "garage/distance/triggered"
#TOPIC_MOTION_TRIGGERED = "garage/motion/triggered"
#TOPIC_LIGHT_TRIGGERED = "garage/light/triggered"
#TOPIC_ACCELERATION_TRIGGERED = "garage/acceleration/triggered"

# Outgoing messages

TOPIC_DANGER_LEVEL = TP_LOCATION + "/" + ST_DANGER_LEVEL
TOPIC_RED_BUTTON_ENABLE = TP_RED_BUTTON + "/" + ST_ENABLE
TOPIC_WHITE_BUTTON_ENABLE = TP_WHITE_BUTTON + "/" + ST_ENABLE
TOPIC_RED_BUTTON_DISABLE = TP_RED_BUTTON + "/" + ST_DISABLE
TOPIC_WHITE_BUTTON_DISABLE = TP_WHITE_BUTTON + "/" + ST_DISABLE

TOPIC_MUSIC_LULLABY = TP_MUSIC + "/lullaby"
TOPIC_MUSIC_WAKEUP = TP_MUSIC + "/wakeup"

TOPIC_VIDEO_SLEEPING = TP_DRAGON + "/sleeping"
TOPIC_VIDEO_SLEEPY = TP_DRAGON + "/sleepy"
TOPIC_VIDEO_WAKEUP = TP_DRAGON + "/wakeup"

TOPIC_LEDSTRIP_FIRE = TP_LOCATION + "/ledstrip/fire"  # arg: int number of times to repeat (approx number of sec)
TOPIC_SMOKE = "smoke/puff/long" # smoke/puff/medium

def restart_controller():
    game.reset()

    client.publish(TOPIC_DANGER_LEVEL, game.danger_level)

    # Set trigger ranges for sensors
    client.publish(TP_DISTANCE + "/" + ST_RANGE_LOW, DISTANCE_LOW)
    client.publish(TP_ACCELERATION + "/" + ST_RANGE_LOW, ACCELERATION_LOW)
    client.publish(TP_LIGHT + "/" + ST_RANGE_LOW, LIGHT_LOW)

    client.publish(TP_DISTANCE + "/" + ST_RANGE_HIGH, DISTANCE_HIGH)
    client.publish(TP_ACCELERATION + "/" + ST_RANGE_LOW, ACCELERATION_HIGH)
    client.publish(TP_LIGHT + "/" + ST_RANGE_LOW, LIGHT_HIGH)

    client.publish(TP_DISTANCE + "/" + ST_TRIGGER_PAUSE, DISTANCE_PAUSE)
    client.publish(TP_ACCELERATION + "/" + ST_TRIGGER_PAUSE, ACCELERATION_PAUSE)
    client.publish(TP_LIGHT + "/" + ST_TRIGGER_PAUSE, LIGHT_PAUSE)
    client.publish(TP_MOTION + "/" + ST_TRIGGER_PAUSE, MOTION_PAUSE)

    client.publish(TOPIC_WHITE_BUTTON_ENABLE, NO_ARG)
    client.publish(TOPIC_RED_BUTTON_DISABLE, NO_ARG)

    client.publish(TOPIC_VIDEO_SLEEPING, NO_ARG)


def on_controller_start(mosq, obj, msg):
    print("MESSAGES: " + msg.topic + " " + str(msg.payload))
    restart_controller()


def on_sensor_triggered(mosq, obj, msg):
    print("MESSAGES: " + msg.topic )
    if not game.is_waking_up:
        # game.danger_level = min(game.danger_level + 25, 100)
        update_danger_level(min(game.danger_level + 25, 100))


def update_danger_level(new_level):
    if new_level >= DANGER_HIGH_THRESHOLD:
        if game.danger_level < DANGER_HIGH_THRESHOLD:
            client.publish(TOPIC_RED_BUTTON_ENABLE, NO_ARG)
            client.publish(TOPIC_VIDEO_SLEEPY, NO_ARG)   # Should have been almost awake video
    elif new_level < DANGER_MEDIUM_THRESHOLD:
        if game.danger_level >= DANGER_MEDIUM_THRESHOLD:
            client.publish(TOPIC_RED_BUTTON_DISABLE, NO_ARG)
            client.publish(TOPIC_VIDEO_SLEEPING, NO_ARG)
    elif (game.danger_level < DANGER_MEDIUM_THRESHOLD) or (game.danger_level >= DANGER_HIGH_THRESHOLD):
        client.publish(TOPIC_VIDEO_SLEEPY, NO_ARG)
        client.publish(TOPIC_RED_BUTTON_DISABLE, NO_ARG)
    game.danger_level = new_level
    client.publish(TOPIC_DANGER_LEVEL, game.danger_level)


def on_delayed_publish(topic):
    client.publish(topic, NO_ARG)


def publish_with_delay(topic, delay):
    ti = threading.Timer(delay, on_delayed_publish, args=(topic,))
    ti.start()


def on_white_button_pressed(mosq, obj, msg):
    print("MESSAGES: " + msg.topic )
    if not game.is_waking_up:
        client.publish(TOPIC_MUSIC_LULLABY, NO_ARG)
        new_level = max(game.danger_level - game.lul_effect, 0)
        # Reduce effect of lullaby each time it is triggered
        game.lul_effect = max(game.lul_effect - 5, 0)
        publish_with_delay(TOPIC_WHITE_BUTTON_ENABLE, PAUSE_FOR_WHITE_BUTTON_REENABLE)
        update_danger_level(new_level)


def on_red_button_pressed(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    game.is_waking_up = True
    client.publish(TOPIC_MUSIC_WAKEUP, NO_ARG)
    client.publish(TOPIC_WHITE_BUTTON_DISABLE, NO_ARG)
    client.publish(TOPIC_RED_BUTTON_DISABLE, NO_ARG)

    publish_with_delay(TOPIC_VIDEO_WAKEUP, PAUSE_BETWEEN_WAKEUP_MUSIC_AND_VIDEO)
    publish_with_delay(TOPIC_SMOKE, PAUSE_BETWEEN_WAKEUP_MUSIC_AND_SMOKE)
    publish_with_delay(TOPIC_LEDSTRIP_FIRE, PAUSE_BETWEEN_WAKEUP_MUSIC_AND_SMOKE)
    publish_with_delay(TOPIC_CONTROLLER_START, PAUSE_FROM_START_OF_WAKEUP_TO_RESTART)


def on_message(client, userdata, message):
    print("topic : ", message.topic)    
    
    
client = mqtt.Client("MainController")
client.on_message=on_message

client.message_callback_add(TOPIC_CONTROLLER_START, on_controller_start)
client.message_callback_add(PATTERN_TRIGGERED, on_sensor_triggered)
client.message_callback_add(TOPIC_WHITE_BUTTON_PRESSED, on_white_button_pressed)
client.message_callback_add(TOPIC_RED_BUTTON_PRESSED, on_red_button_pressed)

client.connect(server_address)
client.loop_start()
client.publish("test/dragondangercontroller/starting", NO_ARG)

client.subscribe(TOPIC_CONTROLLER_START)
client.subscribe(PATTERN_TRIGGERED)
client.subscribe(TOPIC_WHITE_BUTTON_PRESSED)
client.subscribe(TOPIC_RED_BUTTON_PRESSED)
restart_controller()

while True:
    sleep(5)

client.loop_stop()
