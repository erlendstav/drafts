import paho.mqtt.client as mqtt
import time



    
class Step:
    /*
        Start performing the step.
        Returns true if the current script should proceed after this step, or
        false if it should be stop.
    */

    def perform(context):
        print("Default step")
        return true
        
    def waitForCallback():
        return false
    







print("Hello world")