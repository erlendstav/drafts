import paho.mqtt.client as mqtt
from omxplayer.player import OMXPlayer
from pathlib import Path
import time

server_address="10.0.0.2"

def on_playvideo(message):
    if message.topic.endswith("scare"):
        print("Starting video " + message.topic)
    else:
        return

def on_message(client, userdata, message):
    print("topic : ", message.topic)
    on_playvideo(message)
    
#client = mqtt.Client("ErlendsMac")
#client.on_message=on_message
#client.connect(server_address)
#client.loop_start()
#client.subscribe("test/garage/#")
#client.publish("test/state", "Hello from Python")

#while True:
#    time.sleep(5)

#client.loop_stop()

VIDEO_1_PATH = Path("/home/pi/Videos/GA3_Buffer_Black_H.mp4")
VIDEO_2_PATH = Path("/home/pi/Videos/PHA_Spinster_BehaveOrBeDead_Win_H.mp4")
#player_log = logging.getLogger("Player 1")

#player1 = OMXPlayer(VIDEO_1_PATH, dbus_name="no.sintef.mqttvideo.player1")
#player1.pause()
player2 = OMXPlayer(VIDEO_2_PATH, dbus_name="no.sintef.mqttvideo.player2", pause=True)

#        ,dbus_name='org.mpris.MediaPlayer2.omxplayer1')
#player1.playEvent += lambda _: print("Play event triggered") #player_log.info("Play")
#player1.pauseEvent += lambda _: print("Pause event triggered") #player_log.info("Pause")
#player1.stopEvent += lambda _: print("Stop event triggered") #player_log.info("Stop")

player2.playEvent += lambda _: print("Play event triggered for 2") #player_log.info("Play")
player2.pauseEvent += lambda _: print("Pause event triggered for 2") #player_log.info("Pause")
player2.stopEvent += lambda _: print("Stop event triggered for 2") #player_log.info("Stop")

time.sleep(2.5)

player2.play()
# it takes about this long for omxplayer to warm up and start displaying a picture on a rpi3
time.sleep(15.5)

player2.set_position(20)
player2.pause()


time.sleep(2)

#player.set_aspect_mode('stretch')
#player.set_video_pos(0, 0, 200, 200)
player2.play() 

time.sleep(5)
player2.pause()
player2.load(VIDEO_1_PATH)
player2.play()
#player1.play()
time.sleep(5)

#player1.quit()
player2.quit()
