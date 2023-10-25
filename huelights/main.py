from phue import Bridge
from time import sleep

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


b = Bridge('192.168.1.21')

# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()

lights = b.lights
light_named = b.get_light_objects('name')

for l in lights:
    print(l.name, l.light_id)

Hue_Original = 8417
Hue_Plain = 9277
Hue_Green = 18801
Hue_Red = 273
Hue_PurpleBlue = 48671
Hue_Blue = 44963
Hue_WarmOrange = 7207

print("Switch :", light_named["Hue smart plug 1"].on)

print("Play 1 :", light_named["Hue Play 1"].on, light_named["Hue Play 1"].hue, light_named["Hue Play 1"].brightness)
print("Play 2 :", light_named["Hue Play 2"].on, light_named["Hue Play 2"].hue)

light_named["Hue Play 1"].hue = Hue_WarmOrange
sleep(2)

#command =  {'transitiontime' : 50, 'bri' : 200, 'hue' : Hue_Red}
#b.set_light(4, command)
#sleep(6)

#command =  {'transitiontime' : 100, 'bri' : 50, 'hue' : Hue_Green}
#b.set_light(4, command)
#b.set_light(6, command)
#sleep(12)
light_named["Hue Play 1"].transitiontime = 3
light_named["Hue Play 1"].brightness = 100
sleep(2)
light_named["Hue Play 1"].hue = Hue_WarmOrange

sleep(2)
light_named["Hue Play 1"].brightness = 50
sleep(3)
light_named["Hue Play 1"].brightness = 150
sleep(0.5)
light_named["Hue Play 1"].brightness = 50
sleep(3)
light_named["Hue Play 1"].brightness = 200
sleep(0.5)
light_named["Hue Play 1"].brightness = 100
sleep(0.5)
light_named["Hue Play 1"].transitiontime = 1
light_named["Hue Play 1"].on = False
sleep(3)
light_named["Hue Play 1"].on = True
sleep(0.3)
light_named["Hue Play 1"].on = False
sleep(2)
light_named["Hue Play 1"].on = True
sleep(0.2)
light_named["Hue Play 1"].brightness = 170
sleep(0.3)
light_named["Hue Play 1"].brightness = 50
sleep(0.5)
light_named["Hue Play 1"].on = False
sleep(2)
light_named["Hue Play 1"].on = True
sleep(2)


#lights["Hue smart plug 1"].on = True
#sleep(5)
#lights["Hue smart plug 1"].on = False

#for l in lights:
#    print(l.name)
