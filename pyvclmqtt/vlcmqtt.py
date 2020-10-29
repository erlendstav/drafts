import paho.mqtt.client as mqtt
import vlc
from pathlib import Path
import time


#print("Hello world")
#player = vlc.MediaPlayer("/Users/erlendstav/Movies/HalloweenScenario/BOO_BooTime_Win_H.mp4")
#player.play()
#i = player.get_instance
#while True:
#    time.sleep(5)
#
#print("Completed")


# creating vlc media player object 
media_player = vlc.MediaPlayer() 

vlc.MediaPlayer()



# media object 
media = vlc.Media("/Users/erlendstav/Movies/HalloweenScenario/BOO_FlyingBlind_Win_H.mp4") 
  
# setting media to the media player 
media_player.set_media(media) 
  
  
# start playing video 
media_player.play() 

  
# wait so the video can be played for 5 seconds 
# irrespective for length of video 
time.sleep(15) 
  
# getting media 
value = media_player.get_media() 
  
# printing media 
print("Media : ") 
print(value) 

