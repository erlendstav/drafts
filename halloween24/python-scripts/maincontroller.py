import pygame
import paho.mqtt.client as mqtt
import time
#from pythonosc import udp_client
from pythonosc.udp_client import SimpleUDPClient


# init sound players
pygame.init()
pygame.mixer.init()

# init osc client
ip = "localhost"
port = 21600
client = SimpleUDPClient(ip, port)  # Create client

print("Client...")
#baby_laugh_sound = pygame.mixer.Sound(sound_loc + baby_laugh_name)

# loop

while True:
    # Option: Wait for trigger to start

    # Set initial lights and start skeleton music
    pygame.mixer.music.load('SpookyScary.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(0)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/PartyStart/start", "")

    # Wait for trigger or timer to change to red
    time.sleep(30)
    # Set red lights and change music
    pygame.mixer.music.stop()
    pygame.mixer.music.load('OneOfTheseDays.mp3')
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(0)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/PartyGrim/start", "")

    # Wait until time to switch to black light
    time.sleep(44)
    # Switch to black light
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/BlackLightParty/start", "")

    # Wait until time to show good-bye lights
    time.sleep(32)
    client.send_message("/palette/*/stop", "")
    client.send_message("/palette/PartyDone/start", "")
    # Wait a couple of secounds before playing good-bye music
    time.sleep(2)
    # Add check on whether it is playing?
    pygame.mixer.music.stop()
    pygame.mixer.music.load('GoHome.mp3')
    pygame.mixer.music.play(0)
    time.sleep(20)


