"""
gpio interface

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
GPIO Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1gpio.html
"""
import time

from .constants import RPI, MPY, LS, GPS, LORA, FREQ

if RPI:
    ### DEFINE GPIO PINS ###
    # import RPi.GPIO as GPIO
    import busio
    from digitalio import DigitalInOut, Direction, Pull
    import board
if MPY:
    import machine
else:
    import logging
    import datetime

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

### Misc pins
B1 = 5          # GPIO 5 or Pin 29  |
B2 = 6          # GPIO 6 or Pin 12  |
B3 = 12         # GPIO 12 or Pin 32 |

SPI = None
rfm9x = None
RTC = machine.RTC()


def ls_event(pin) -> int:
    """ Lightning Sensor Interrupt Pin Rising Event Handler
    
    Args:
        None
    Returns:
        None
    """
    if MPY:
        print("Rising Lightning Event!")
    else:
        logging.info("\t%s\t|\tRising Lightning Event on pin %d!", __name__, pin)
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
        # GPIO.setmode(GPIO.BCM)

        ## GPIO.setup
        # GPIO.setup(B1, GPIO.IN)
        # GPIO.setup(B2, GPIO.IN)
        # GPIO.setup(B3, GPIO.IN)
        # GPIO.setup(LS_IRQ, GPIO.IN)

        ### Communication Protocols
        I2C1 = busio.I2C(board.GP7, board.GP6)          # Create the first I2C interface
        I2C2 = busio.I2C(board.GP7, board.GP6)          # Create the second I2C interface
        SPI = busio.SPI(CLK, MOSI=DI, MISO=DO)          # Create the SPI interface
        UART = busio.UART(tx=board.GP0, rx=board.GP1, baudrate=9600, timeout=10)

        ### Initialize Modules
        if GPS:
            import adafruit_gps             # GPS Module
            gps_module = adafruit_gps.GPS(UART, debug=False)   # Use UART/pyserial
            # Turn on the basic GGA and RMC info (what you typically want)
            gps_module.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
            # Set update rate to once a second (1hz) which is what you typically want.
            gps_module.send_command(b"PMTK220,1000")

            # Wait until the GPS obtains a fix
            while not gps_module.has_fix:
                print("Waiting for fix...")
                time.sleep(1)

            # Set RTC using Fix timestamp
            rtc.datetime((
                gps_module.timestamp_utc.tm_year,
                gps_module.timestamp_utc.tm_mon,
                gps_module.timestamp_utc.tm_mday,
                gps_module.timestamp_utc.tm_hour,
                gps_module.timestamp_utc.tm_min,
                gps_module.timestamp_utc.tm_sec,
                0,
                0,
            ))

            # Store GPS location
            # gps.latitude_degrees, gps.latitude_minutes
            # gps.longitude_degrees, gps.longitude_minutes
            # gps.fix_quality
            # gps.satellites
            # gps.altitude_m
            # gps.speed_knots
            gps_packet: str = f"STK:{rtc()},{gps_module.latitude_degrees},{gps_module.longitude_degrees}"

            # Turn off GPS


        if LS:
            import sparkfun_qwiicas3935     # Lightning Module
            # Create as3935 object
            lightning = sparkfun_qwiicas3935.Sparkfun_QwiicAS3935_I2C(I2C1)

            # Check if connected
            if lightning.connected:
                print("Schmow-ZoW, Lightning Detector Ready!")
            else:
                print("Lightning Detector does not appear to be connected. Please check wiring.")
                # sys.exit()

            # Set Mode
            lightning.indoor_outdoor = lightning.OUTDOOR
            afe_mode = lightning.indoor_outdoor
            if afe_mode == lightning.OUTDOOR:
                print("The Lightning Detector is in the Outdoor mode.")
            elif afe_mode == lightning.INDOOR:
                print("The Lightning Detector is in the Indoor mode.")
            else:
                print("The Lightning Detector is in an Unknown mode.")

            # Callibrate
            # TODO: describe
            lightning.noise_level = 5           # (1-7, default=2)
            lightning.watchdog_threshold = 2    # (1-10, default=2)
            lightning.spike_rejection = 1       # (1-11, default=2)

        if LORA:
            ## Setup LoRa Radio
            import adafruit_rfm9x       # LORA Module
            global rfm9x
            lora_cs = DigitalInOut(board.CE1)
            lora_rst = DigitalInOut(board.D25)
            rfm9x = adafruit_rfm9x.RFM9x(SPI, lora_cs, lora_rst, FREQ)
            rfm9x.tx_power = 23

            ## Setup OLED and attached buttons
            import adafruit_ssd1306     # OLED Module
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
            display = adafruit_ssd1306.SSD1306_I2C(128, 32, I2C2, reset=reset_pin)
            # Clear the display.
            display.fill(0)
            display.show()
            width = display.width
            height = display.height

        ## Event Detectors for buttons and Lightning Sensor
        if LS:
            GPIO.add_event_detect(LS_IRQ, GPIO.RISING, callback=ls_event)
        else:
            GPIO.add_event_detect(B1, GPIO.RISING, callback=ls_event)

        # Return Name?

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
        with open(file='/sys/class/thermal/thermal_zone0/temp', encoding='utf8') as f:
            logging.info("\t%s\t|\tCurrent CPU temp = %f", __name__, float(f.read())/1000)
    else:
        logging.info("\t%s\t|\tTemperature Check on a non-RPi", __name__)

def lora_tx(packet:str) -> None:
    """ Sends the packet
    
    Args:
        packet (str): The packet to be sent over LoRa
    Returns:
        None
    """
    if RPI:
        if LORA:
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

# def gps() -> str:
#     """ Acquires and returns GPS data in NMEA form

#     This method should extract the Latitude and Longitude from the NMEA data.
#     We may add GPS RTC features later as well

#     Args:
#         None
#     Returns:
#         nmea (str): a string that combines latitude and longitude in a string ready for LoRa

#     """
#     if RPI:
#         if GPS:
#             nmea = "loc"
#         else:
#             nmea = "disabled"
#     else:
#         nmea = "gps"
#     logging.info("\t%s\t|\t* GPS NMEA Data = %s", __name__, nmea)
#     return f"GPS:{nmea}"

def rtc() -> str:
    """ Acquire current time from Real Time Clock Module

    Args:
        None
    Returns:
        time (str): current time
    """
    if MPY:
        time = RTC.datetime()
    else:
        time = datetime.datetime()
    return time

def lightning() -> str:
    """ Interacts with the Lightning Sensor Module

    Args:
        None
    Returns:
        ls_out (str): a concatenated string with sensor data for the packet

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
        # This allows us to simulate the strike with a keypress on a non rpi device
        # keyboard.wait("c")
        time.sleep(2)
        # Mock Data
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
        if MPY:
            print("Cleaning up GPIO pins...")
        else:
            logging.info("\t%s\t|\tCleaning up GPIO pins", __name__)
        GPIO.cleanup()