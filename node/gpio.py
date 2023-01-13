"""
gpio interface
"""
import logging
from .constants import RPI

### Shared Pins
DI = 10         # GPIO 10 or Pin 19 | LoRa DI or LS MOSI
DO = 9          # GPIO 9 or Pin 21  | LoRa DO or LS MISO
CLK = 11        # GPIO 11 or Pin 23 | Clock

### LoRa - SPI
LORA_CS = 7     # GPIO 7 or Pin 26  | arbitrary - control select
LORA_RST = 25   # GPIO 25 or Pin 22 | arbitrary - reset

### Lightning Module - SPI
LS_CS = 8       # GPIO 8 or Pin 24  | arbitrary - control select
LS_IRQ = 13     # GPIO 13 or Pin 33 | arbitrary - interrupt

### GPS - UART
GPS_TX = 14     # GPIO 14 or Pin 8  | TX
GPS_RX = 15     # GPIO 15 or Pin 10 | RX
GPS_1PPS = 17   # GPIO 17 or Pin 11 | 1 Pulse Per second on GPS RTC
GPS_RTC = 18    # GPIO 18 or Pin 12 | RTC
GPS_3D = 27     # GPIO 27 or Pin 13 | TODO: What does this do?
GPS_RST = 4     # GPIO 4 or Pin 7   | arbitrary - RST

### RTC - I2C
RTC_SDA = 0     # GPIO 0 or Pin 27  | arbitrary? - SDA
RTC_SCL = 1     # GPIO 1 or Pin 28  | arbitrary? - SCL
RTC_SQW = 26    # GPIO 26 or Pin 37 | arbitrary? - Square Wave
RTC_RST = 19    # GPIO 19 or Pin 35 | arbitrary - reset

### OLED - I2C
OLED_SDA = 2    # GPIO 2 or Pin 3   | arbitrary? - SDA
OLED_SCL = 3    # GPIO 3 or Pin 5   | arbitrary? - SCL

### Misc pins
B1 = 5          # GPIO 5 or Pin 29  |
B2 = 6          # GPIO 6 or Pin 12  |
B3 = 12         # GPIO 12 or Pin 32 |

if RPI:
    ### DEFINE GPIO PINS ###
    import RPi.GPIO as GPIO
    import adafruit_rfm9x

    # FROM LORAMESH EX
    from network import LoRa
    import socket
    import time
    import ubinascii
    import py_com
    from loramesh import Loramesh


    import busio
    SPI = busio.SPI(CLK, MOSI=DI, MISO=DO)

    import smbus

def BtnEventHandler_rising(pin):
    logging.info("Rising Button Event on pin %d!", pin)
    return 0

def BtnEventHandler_falling(pin):
    logging.info("Falling Button Event on pin %d!", pin)
    return 0

def LSEventHandler_rising(pin):
    logging.info("Rising Lightning Sensor Event on pin %d!", pin)
    return 0

def LSEventHandler_falling(pin):
    logging.info("Falling Lightning Sensor Event on pin %d!", pin)
    return 0

def setup():
    """
    Initializes RPI GPIO pins
    """
    try:
        if RPI:
            GPIO.setmode(GPIO.BCM)
            ## GPIO.setup
            GPIO.setup(B1, GPIO.IN)
            GPIO.setup(B2, GPIO.IN)
            GPIO.setup(B3, GPIO.IN)
            ## GPIO.output

            ## Event Detectors for buttons and Lightning Sensor
            GPIO.add_event_detect(B1, GPIO.RISING, callback=BtnEventHandler_rising)
            GPIO.add_event_detect(B1, GPIO.FALLING, callback=BtnEventHandler_falling)
            GPIO.add_event_detect(B2, GPIO.RISING, callback=BtnEventHandler_rising)
            GPIO.add_event_detect(B2, GPIO.FALLING, callback=BtnEventHandler_falling)
            GPIO.add_event_detect(B3, GPIO.RISING, callback=BtnEventHandler_rising)
            GPIO.add_event_detect(B3, GPIO.FALLING, callback=BtnEventHandler_falling)
            GPIO.add_event_detect(LS_IRQ, GPIO.RISING, callback=LSEventHandler_rising)
            GPIO.add_event_detect(LS_IRQ, GPIO.FALLING, callback=LSEventHandler_falling)

            rfm9x = adafruit_rfm9x.RFM9x(SPI, LORA_CS, LORA_RST, 915.0)
            rfm9x.tx_power = 23
    except:
        cleanup()
    return 0

def gps():
    if RPI:
        nmea = "loc"
    else:
        nmea = "gps"
    return f"GPS:{nmea}"

def rtc() -> str:
    """
    Interacts with the Real Time Clock Module
    """
    if RPI:
        time = "1"
    else:
        time = "rtc"
    return time

def lightning() -> str:
    """
    Interacts with the Lightning Sensor Module

    FIXME: TODO: Simulate this with a button input first, then add lightning sensor later

    GPIO Pins Involved:
    - CS ["Chip Select"]: Pull low to activate SPI reception
    - IRQ ["Interrupt request"]: Triggers when a strike is detected
    - SCL: Clock
    - MISO: Data from AS3935 to microcontroller
    - MOSI: Data from microcontroller to AS3935

    """
    if RPI:
        distance = "2"
        intensity = "3"
    else:
        distance = "distance"
        intensity = "intensity"
    return f"{distance},{intensity}"

def cleanup():
    if RPI:
        logging.info("Cleaning up GPIO pins")
        GPIO.cleanup()
    return 0