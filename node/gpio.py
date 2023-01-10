"""
gpio interface
"""
from .constants import RPI

if RPI:
    ### DEFINE GPIO PINS ###
    import adafruit_rfm9x  # LoRa
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.board)
    ## GPIO.setup
    ## GPIO.output

def setup():
    """
    Initializes RPI GPIO pins
    """
    return 0