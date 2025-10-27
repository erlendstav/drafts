import paho.mqtt.client as mqtt
import time

server_address="192.168.1.50"
client_name = "GarageMainController"

# MQTT Topics
TOPIC_LOCATION = "garage"
TOPIC_VIDEO = TOPIC_LOCATION + "/video"
TOPIC_MUSIC = TOPIC_LOCATION + "/music"
TOPIC_LIGHT = TOPIC_LOCATION + "/light"
TOPIC_SOUND = TOPIC_LOCATION + "/sound"
TOPIC_START = TOPIC_LOCATION + "/start"

# Scare levels
LVL_FRIENDLY = "friendly"
#LVL_NORMAL = "normal"
LVL_SCARY = "scary"

# MQTT Topics listened to
TOPIC_START_FRIENDLY = TOPIC_START + "/" + LVL_FRIENDLY
#TOPIC_START_NORMAL = TOPIC_START + "/" + LVL_NORMAL
TOPIC_START_SCARY = TOPIC_START + "/" + LVL_SCARY
TOPIC_MOVEMENT = TOPIC_LOCATION + "/movement"
TOPIC_VIDEO_DONE = TOPIC_LOCATION + "/video/done"

# MQTT Topics sent to other components
#TOPIC_LIGHT_START = TOPIC_LIGHT + "/start" 
TOPIC_LIGHT_SUMMON = TOPIC_LIGHT + "/summon" 

TOPIC_LIGHT_START_FRIENDLY = TOPIC_LIGHT + "/start/" + LVL_FRIENDLY
TOPIC_LIGHT_START_SCARY = TOPIC_LIGHT + "/start/" + LVL_SCARY
TOPIC_LIGHT_EXIT = TOPIC_LIGHT + "/exit"
TOPIC_LIGHT_DARK = TOPIC_LIGHT + "/dark"

TOPIC_SOUND_SUMMON = TOPIC_SOUND + "/summon"

TOPIC_MUSIC_FRIENDLY = TOPIC_LOCATION + "/music/friendly"
TOPIC_MUSIC_SCARY = TOPIC_LOCATION + "/music/scary"
TOPIC_MUSIC_STOP = TOPIC_LOCATION + "/music/stop"

# Timing constants
SUMMON_EFFECT_DURATION = 15 # seconds
MOVEMENT_IGNORE_DURATION = 15  # seconds

start_time = time.time()
scare_level = LVL_FRIENDLY
summon_started = False


''' 
The scenario is started and the scare level is set with 
messages that start with garage/start/.
Levels can be friendly, normal, or scary.

When the scenario is started, the background music for the scare level starts, 
the light is set to starting configuration for the scare level,
and a timer is started.

When movement is detected at least 15 seconds after the scenario stated, 
the music is stopped, and the sound effect and light for the summoning ritual is triggered 
for the current scare level.

When the summoning sound is completed, the lights are turned off and the video for the scare level is played.

When the video is completed, the lights is set to exit configuration.
'''


def on_start_friendly(mosq, obj, msg):
    global start_time 
    global summon_started
    start_time = time.time()
    summon_started = False
    print("MESSAGES: " + msg.topic)
    client.publish(TOPIC_LIGHT_START_FRIENDLY, "1") 
    client.publish(TOPIC_MUSIC_FRIENDLY, "1")


def on_start_scary(mosq, obj, msg):
    global start_time 
    global summon_started
    start_time = time.time()
    summon_started = False
    print("MESSAGES: " + msg.topic)
    client.publish(TOPIC_LIGHT_START_SCARY, "1")
    client.publish(TOPIC_MUSIC_SCARY, "1")


def on_movement(mosq, obj, msg):
    global start_time
    global summon_started
    if summon_started:
        print("Ignoring movement, summon already started")
        return
    current_time = time.time()
    elapsed = current_time - start_time
    print("MESSAGES: " + msg.topic + " elapsed time since start: " + str(elapsed))
    if elapsed < MOVEMENT_IGNORE_DURATION:
        print("Ignoring movement event, too soon after start")
        return
    client.publish(TOPIC_MUSIC_STOP, "1")
    client.publish(TOPIC_LIGHT_SUMMON + "/" + scare_level, "1")
    client.publish(TOPIC_SOUND_SUMMON + "/" + scare_level, "1")
    time.sleep(SUMMON_EFFECT_DURATION)
    client.publish(TOPIC_LIGHT_DARK, "1")  # Wait for sound to start
    client.publish(TOPIC_VIDEO + "/" + scare_level, "1")    


def on_video_done(mosq, obj, msg):
    print("MESSAGES: " + msg.topic)
    client.publish(TOPIC_LIGHT_EXIT, "1")


def on_message(client, userdata, message):
    print("Ignoring message " + message.topic)


def setup_mqtt():
    c = mqtt.Client(client_name)
    c.on_message=on_message
    c.message_callback_add(TOPIC_START_FRIENDLY, on_start_friendly)
    c.message_callback_add(TOPIC_START_SCARY, on_start_scary)
    c.message_callback_add(TOPIC_MOVEMENT, on_movement)
    c.message_callback_add(TOPIC_VIDEO_DONE, on_video_done)

    c.connect(server_address)
    c.loop_start()
    return c


# Main program starts here
client = setup_mqtt()
client.subscribe("garage/#")
client.publish("test/hello", "Hello from " + client_name)

while True:
    time.sleep(10)
    client.publish("status/alive/" + client_name)

client.loop_stop()