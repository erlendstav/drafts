import pygame
import paho.mqtt.client as mqtt
import time
from pythonosc import udp_client

# init sound players
pygame.init()
pygame.mixer.init()

client = udp_client.SimpleUDPClient(args.ip, args.port)

print("Client...")
#baby_laugh_sound = pygame.mixer.Sound(sound_loc + baby_laugh_name)

# loop

while True:
    # Option: Wait for trigger to start

    # Set initial lights and start skeleton music
    pygame.mixer.music.load('SpookyScary.mp3')
    pygame.mixer.music.play(-1)
    client.send_message("/filter", random.random())

    # Wait for trigger or timer to change to red
    time.sleep(30)
    # Set red lights and change music
    pygame.mixer.music.stop()
    pygame.mixer.music.load('OneOfTheseDays.mp3')
    pygame.mixer.music.play(-1)
    client.send_message("/filter", random.random())

    # Wait until time to switch to black light
    time.wait(45)
    # Switch to black light
    client.send_message("/filter", random.random())

    # Wait until time to show good-bye lights
    time.wait(45)
    client.send_message("/filter", random.random())
    # Wait a couple of secounds before playing good-bye music
    time.wait(2)
    # Add check on whether it is playing?
    pygame.mixer.music.stop()
    pygame.mixer.music.load('GoHome.mp3')
    pygame.mixer.music.play(-1)


