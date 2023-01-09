""" __init__.py
"""
from .LoRa import send
from .sensor import collect

import logging
import platform
# RPI = False
# if platform.system() == "Linux":
#     if platform.release().find('raspi'):
#         print("THIS IS A RASPBIAN SYSTEM\n")
#         RPI = True

# import RPi.GPIO as GPIO     # GPIO
# import adafruit_rfm9x       # LoRa