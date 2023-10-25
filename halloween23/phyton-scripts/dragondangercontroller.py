import paho.mqtt.client as mqtt
from struct import *
from time import sleep
import os
import json
from enum import Enum

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


game = GameState(0, False)


# accept ranges in mm
# bat_distance_min = 200.0
# bat_distance_max = 400.0

DISTANCE_LOW = 20
DISTANCE_HIGH = 1000

ACCELERATION_LOW = 200
ACCELERATION_HIGH = 400

LIGHT_LOW = 200
LIGHT_HIGH = 400

# spider_x_min = 15.0
# spider_x_max = 30.0
# spider_y_min = 15.0
# spider_y_max = 30.0

# box_light_min = 30.0
# box_light_max = 70.0

# Subtopics and topic prefix
ST_PRESSED = "pressed"
ST_TRIGGERED = "triggered"
ST_ENABLED = "enabled" # true / false
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
TOPIC_RED_BUTTON_ENABLED = TP_RED_BUTTON + "/" + ST_ENABLED
TOPIC_WHITE_BUTTON_ENABLED = TP_WHITE_BUTTON + "/" + ST_ENABLED
TOPIC_MUSIC_LULLABY = TP_MUSIC + "/lullaby"
TOPIC_MUSIC_WAKEUP = TP_MUSIC + "/wakeup"

TOPIC_VIDEO_SLEEPING = TP_DRAGON + "/sleeping"
TOPIC_VIDEO_SLEEPY = TP_DRAGON + "/sleepy"
TOPIC_VIDEO_WAKEUP = TP_DRAGON + "/wakeup"


def restart_controller():
    game.reset()

    client.publish(TOPIC_DANGER_LEVEL, game.danger_level)

    # Set trigger ranges for sensors
    client.publish(TP_DISTANCE + "/" + ST_RANGE_LOW, DISTANCE_LOW)
    client.publish(TP_ACCELERATION + "/" + ST_RANGE_LOW, ACCELERATION_LOW)
    client.publish(TP_LIGHT + "/" + ST_RANGE_LOW, LIGHT_LOW)

    sleep(1)

    client.publish(TP_DISTANCE + "/" + ST_RANGE_HIGH, DISTANCE_HIGH)
    client.publish(TP_ACCELERATION + "/" + ST_RANGE_LOW, ACCELERATION_HIGH)
    client.publish(TP_LIGHT + "/" + ST_RANGE_LOW, LIGHT_HIGH)

    client.publish(TOPIC_WHITE_BUTTON_ENABLED, True)
    client.publish(TOPIC_RED_BUTTON_ENABLED, False)

    client.publish("dragon/sleeping", "Sleep")


def on_controller_start(mosq, obj, msg):
    print("MESSAGES: " + msg.topic + " " + str(msg.payload))
    restart_controller()


def on_controller_check(mosq, obj, msg):
    if game.is_waking_up:
        return
    game.is_waking_up = True
    print("MESSAGES: " + msg.topic + " " + str(msg.payload))
    print("Sensor status : ", game.sensors)
#   print("Bat distance : ", bat_status, " ", game.bat_distance)
#    print("Spider x     : ", spider_x_status, " ", game.spider_x)
#    print("Spider y     : ", spider_y_status, " ", game.spider_y)
#    print("Box light    : ", box_light_status, " ", game.box_light)
#    if bat_status == spider_x_status == spider_y_status == box_light_status == RangeStatus.OK:
    if all(x == RangeStatus.OK for x in game.sensors.values()):
#        client.publish("bat/sound/wakeup", "Hi")
#        client.publish("ghost/sound/wakeup", "Hi")
#        client.publish("spider/sound/wakeup", "Hi")
#        sleep(5)
        client.publish("dragon/wakeup", "Hi")
    else:
        client.publish("dragon/sleepy", "Hi")
        sleep(2)
        game.is_waking_up = False


def on_sensor_triggered(mosq, obj, msg):
    print("MESSAGES: " + msg.topic )
    if not game.is_waking_up:
        game.danger_level = min(game.danger_level + 25, 100)
        client.publish(TOPIC_DANGER_LEVEL, game.danger_level)


DANGER_MEDIUM_THRESHOLD = 60
DANGER_HIGH_THRESHOLD = 98


def update_danger_level(new_level):
    if new_level >= DANGER_HIGH_THRESHOLD:
        if game.danger_level < DANGER_HIGH_THRESHOLD:
            client.publish(TOPIC_RED_BUTTON_ENABLED, True)
            client.publish(TOPIC_VIDEO_SLEEPY, "hi")
    elif new_level < DANGER_MEDIUM_THRESHOLD:
        if game.danger_level >= DANGER_MEDIUM_THRESHOLD:
            client.publish(TOPIC_RED_BUTTON_ENABLED, False)
            client.publish(TOPIC_VIDEO_SLEEPING, "hi")
    elif (game.danger_level < DANGER_MEDIUM_THRESHOLD) or (game.danger_level >= DANGER_HIGH_THRESHOLD):
        client.publish(TOPIC_VIDEO_SLEEPY, "hi")
        client.publish(TOPIC_RED_BUTTON_ENABLED, False)
    game.danger_level = new_level


def on_white_button_pressed(mosq, obj, msg):
    print("MESSAGES: " + msg.topic )
    if not game.is_waking_up:
        client.publish(TOPIC_MUSIC_LULLABY, "hi")
        game.danger_level = max(game.danger_level - game.lul_effect, 0)
        # Reduce effect of lullaby each time it is triggered
        game.lul_effect = max(game.lul_effect - 5, 0)
        client.publish(TOPIC_DANGER_LEVEL, game.danger_level)


def on_red_button_pressed(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    game.is_waking_up = True
    client.publish(TOPIC_MUSIC_WAKEUP, "hi")
    client.publish(TOPIC_WHITE_BUTTON_ENABLED, False)
    client.publish(TOPIC_RED_BUTTON_ENABLED, False)

    sleep(10)
    client.publish(TOPIC_VIDEO_WAKEUP, "hi")

    sleep(30)
    restart_controller()


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
client.subscribe(TOPIC_CONTROLLER_START)
client.subscribe(PATTERN_TRIGGERED)
client.subscribe(TOPIC_WHITE_BUTTON_PRESSED)
client.subscribe(TOPIC_RED_BUTTON_PRESSED)
# sensor/distance sensor/orientation/x sensor/orientation/y sensor/light  values: "low" "high" "ok"

while True:
    sleep(5)

client.loop_stop()
