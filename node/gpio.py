"""
gpio interface

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
GPIO Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1gpio.html
"""
import logging
import time

from .constants import RPI, LS, RTC, GPS, LORA, FREQ

### FLAGS
LS_FLAG = False

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

SPI = None
rfm9x = None

if RPI:
    ### DEFINE GPIO PINS ###
    import RPi.GPIO as GPIO
    import busio
    from digitalio import DigitalInOut, Direction, Pull
    import board
    import smbus
    import adafruit_ssd1306     # OLED Module
    import adafruit_rfm9x       # LORA Module

    # FROM LORAMESH EX
    # from network import LoRa
    # import socket
    # import ubinascii
    # import py_com
    # from loramesh import Loramesh


def btn_event(pin) -> int:
    """ Debug Button Rising Event Handlers
    
    Args:
        None
    Returns:
        None
    
    TODO: Remove Later
    """
    logging.info("Rising Button Event on pin %d!", pin)
    global LS_FLAG
    LS_FLAG = True
    return 0

def ls_event(pin) -> int:
    """ Lightning Sensor Interrupt Pin Rising Event Handler
    
    Args:
        None
    Returns:
        None
    """
    logging.info("Rising Lightning Sensor Event on pin %d!", pin)
    global LS_FLAG
    LS_FLAG = True
    return 0

def setup() -> None:
    """ Initializes RPI GPIO pins
    
    Args:
        None
    Returns:
        None
    """
    if RPI:
        GPIO.setmode(GPIO.BCM)

        ## GPIO.setup
        GPIO.setup(B1, GPIO.IN)
        GPIO.setup(B2, GPIO.IN)
        GPIO.setup(B3, GPIO.IN)
        GPIO.setup(LS_IRQ, GPIO.IN)

        ### Communication Protocols
        global I2C, SPI
        I2C = busio.I2C(board.SCL, board.SDA)       # Create the I2C interface
        SPI = busio.SPI(CLK, MOSI=DI, MISO=DO)      # Create the SPI interface

        ## GPIO.output

        ## Event Detectors for buttons and Lightning Sensor
        GPIO.add_event_detect(LS_IRQ, GPIO.RISING, callback=ls_event)
        GPIO.add_event_detect(B1, GPIO.RISING, callback=btn_event)

        if LORA:
            ## Setup LoRa Radio
            global rfm9x
            lora_cs = DigitalInOut(board.CE1)
            lora_rst = DigitalInOut(board.D25)
            rfm9x = adafruit_rfm9x.RFM9x(SPI, lora_cs, lora_rst, 915.0)
            rfm9x.tx_power = 23

            ## Setup OLED and attached buttons
            # Button A
            btnA = DigitalInOut(board.D5)
            btnA.direction = Direction.INPUT
            btnA.pull = Pull.UP

            # Button B
            btnB = DigitalInOut(board.D6)
            btnB.direction = Direction.INPUT
            btnB.pull = Pull.UP

            # Button C
            btnC = DigitalInOut(board.D12)
            btnC.direction = Direction.INPUT
            btnC.pull = Pull.UP

            # 128x32 OLED Display
            reset_pin = DigitalInOut(board.D4)
            display = adafruit_ssd1306.SSD1306_I2C(128, 32, I2C, reset=reset_pin)
            # Clear the display.
            display.fill(0)
            display.show()
            width = display.width
            height = display.height

def temp_check() -> None:
    """ Checks the current CPU Temperature from the RPi files
    
    Args:
        None
    Returns:
        None
    
    TODO: Add thresholds for different levels of warnings
    TODO: Add a return to shutdown if too hot
    """
    if RPI:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            logging.info("\t%s\t|\tCurrent CPU temp = %f", __name__, float(f.read())/1000)
    else:
        print()
        logging.info("\t%s\t|\tTemperature Check on a non-RPi", __name__)

def lora_tx(packet:str) -> None:
    """ Sends the packet
    
    Args:
        packet (str): The packet to be sent over LoRa
    Returns:
        None
    """
    if RPI:
        if LORA:    #global?
            encoded_packet = packet.encode('utf-8')
            rfm9x.send(bytearray(encoded_packet))

def lora_rx() -> str:
    """ Checks for incoming LoRa packet

    Checks once and carrys on, any extended checking must be external

    Args:
        None
    Returns:
        pack (str): The packet received over LoRa
    """
    if RPI:
        if LORA:    #global?
            packet = rfm9x.receive()
        else:
            packet = "disabled"
    else:
        packet = "windows"
    return packet

def gps() -> str:
    """ Acquires and returns GPS data in NMEA form

    This method should extract the Latitude and Longitude from the NMEA data.
    We may add GPS RTC features later as well

    Args:
        None
    Returns:
        nmea (str): a string that combines latitude and longitude in a string ready for LoRa

    """
    if RPI:
        if GPS:
            nmea = "loc"
        else:
            nmea = "disabled"
    else:
        nmea = "gps"
    logging.info("* GPS NMEA Data\t=\t%s", nmea)
    return f"GPS:{nmea}"

def rtc() -> str:
    """ Acquire current time from Real Time Clock Module

    Args:
        None
    Returns:
        time (str): current time
    """
    if RPI:
        if RTC:
            time = "2"
        else:
            time = "disabled"
    else:
        time = "rtc"
    return time

def lightning() -> str:
    """ Interacts with the Lightning Sensor Module

    Args:
        None
    Returns:
        ls_out (str): a concatenated string with sensor data for the packet

    FIXME: TODO: Simulate this with a button input first, then add lightning sensor later

    GPIO Pins Involved:
    - CS ["Chip Select"]: Pull low to activate SPI reception
    - IRQ ["Interrupt request"]: Triggers when a strike is detected
    - SCL: Clock
    - MISO: Data from AS3935 to microcontroller
    - MOSI: Data from microcontroller to AS3935

    """
    global LS_FLAG
    if RPI:
        if LS:
            while LS_FLAG is False:
                time.sleep(.1)
            distance = "2"
            intensity = "3"
        else:
            while LS_FLAG is False:
                time.sleep(.1)
            distance = "disabled"
            intensity = "disabled"
    else:
        time.sleep(2)
        distance = "distance"
        intensity = "intensity"
    ls_out = f"{distance},{intensity}"
    LS_FLAG = False
    return ls_out

def cleanup() -> None:
    """ Cleanup GPIO pins before shutdown if RPi is active
    
    Args:
        None
    Returns:
        None
    """
    if RPI:
        logging.info("Cleaning up GPIO pins")
        GPIO.cleanup()