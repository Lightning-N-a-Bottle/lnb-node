"""
Sensor Thread
This file in the module will handle the packaging of sensor data
It will be responsible for the GPIO interface with sensor equipment
"""
import logging
from .constants import RPI
if RPI is True:         # TODO: Maybe add an additional file for GPIO operations?
    ### DEFINE GPIO PINS ###
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.board)
    ## GPIO.setup
    ## GPIO.output

    # GPS
    TX = 14
    RX = 15

    # Lightning Sensor
    CS = 5 # arbitrary - control select
    IRQ = 6 # arbitrary pin, used to indicate that lightning was detected
    SCL = 3
    MISO = 9
    MOSI = 10

    # GPIO.add_event_detect()

    # RTC
    RST = 17 # arbitrary
    SDA = 2
    SCL = 3

def lightning_sensor() -> int:
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
    # if IRQ
    return -1

def rtc_module() -> str:
    """
    Interacts with the Real Time Clock Module
    """
    return ""

def collect() -> str:
    """
    This thread will handle all communications with the sensors and create new packets

    TODO: Sensor Flowchart

    TODO: RTC interface
    TODO: Lightning sensor interface
    TODO: Packet creating
    FIXME: Does GPS go here or with LoRa?
    """
    fmt_sensor = "%(asctime)s | Sensor\t\t: %(message)s"
    logging.basicConfig(format=fmt_sensor, level=logging.INFO,
                        datefmt="%H:%M:%S")
    lightning_detected = -1

    while not lightning_detected:       # This can and should be blocking
        lightning_detected = lightning_sensor()

    # Acquire Lightning Distance/Intensity

    # Acquire RTC Timestamp
    tstmp = rtc_module()

    # Append to PACKET_QUEUE
    packet = tstmp + str(lightning_detected)
    logging.info("\t__name__=%s\t|\tpacket=%s", __name__, packet)

    return packet

if __name__ == "__main__":
    ### Main Block for Sensors - this will only be run if using Sensors individually
    # Configuring startup settings
    FMT = "%(asctime)s | Sensor\t\t: %(message)s"
    logging.basicConfig(format=FMT, level=logging.INFO,
                        datefmt="%H:%M:%S")

    PACKET_QUEUE = []
    PACKET_QUEUE.append(collect())
    logging.info("\"collect()\" function returned with code %s", PACKET_QUEUE)
