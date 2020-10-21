import paho.mqtt.client as mqtt
from omxplayer.player import OMXPlayer
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

VIDEO_1_PATH = "../Videos/PHA_Spinster_BehaveOrBeDead_Win_H.mp4"
#player_log = logging.getLogger("Player 1")

player = OMXPlayer(VIDEO_1_PATH, 
        dbus_name='org.mpris.MediaPlayer2.omxplayer1')
player.playEvent += lambda _: print("Play event triggered") #player_log.info("Play")
player.pauseEvent += lambda _: print("Pause event triggered") #player_log.info("Pause")
player.stopEvent += lambda _: print("Stop event triggered") #player_log.info("Stop")

# it takes about this long for omxplayer to warm up and start displaying a picture on a rpi3
sleep(2.5)

player.set_position(5)
player.pause()


sleep(2)

player.set_aspect_mode('stretch')
player.set_video_pos(0, 0, 200, 200)
player.play()

sleep(5)

player.quit()
