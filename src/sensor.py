"""
Sensor Thread Main
"""
import logging
import time
import os

# TODO: How can we set this up to automate testing?
### DEFINE GPIO PINS ###
## GPIO.setmode
## GPIO.setup
# GPS
TX = 14
RX = 15
# Lightning Sensor
CS = 5 # arbitrary
IRQ = 6 # arbitrary
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
    return -1;

def rtc_module() -> str:
    return ""

def run() -> int:
    """
    This thread will handle all communications with the sensors and create new packets

    TODO: Sensor Flowchart

    TODO: RTC interface
    TODO: Lightning sensor interface
    TODO: Packet creating
    FIXME: Does GPS go here or with LoRa?
    """
    format = "%(asctime)s | Sensor\t\t: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    lightning_detected = -1

    while not lightning_detected:       # This can and should be blocking
        lightning_detected = lightning_sensor()

    # Acquire Lightning Distance/Intensity

    # Acquire RTC Timestamp
    tstmp = rtc_module()

    # Append to PACKET_QUEUE
    PACKET = tstmp + str(lightning_detected)
    logging.info(f"\t{__name__=}\t|\t{PACKET=}")
    time.sleep(1)

    return PACKET

if __name__ == "__main__":
    ### Main Block for Sensors - this will only be run if using Sensors individually
    # Configuring startup settings
    format = "%(asctime)s | Sensor\t\t: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    PACKET_QUEUE = []
    PACKET_QUEUE.append(run())
    logging.info(f"\"run()\" function returned with code {PACKET_QUEUE}")
