"""
gpio interface

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
GPIO Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1gpio.html
"""
import time
import sys

from .constants import RPI, GPS, LS, NOISE_FLOOR, WATCHDOG_THRESH, SPIKE_REJECT#, LORA, FREQ, TX_POW

# import RPi.GPIO as GPIO
import busio
import digitalio
import board
import rtc

class Devices:
    """ Class to interact with all modules """

    ### DEFINE GPIO PINS ###
    ### Shared Pins
    DI = 10         # GPIO 10 or Pin 19 | LoRa DI or LS MOSI
    DO = 9          # GPIO 9 or Pin 21  | LoRa DO or LS MISO
    CLK = 11        # GPIO 11 or Pin 23 | Clock

    ### Misc pins
    B1 = 5          # GPIO 5 or Pin 29  |
    B2 = 6          # GPIO 6 or Pin 12  |
    B3 = 12         # GPIO 12 or Pin 32 |

    def __init__(self) -> None:
        """ Initializes RPI GPIO pins

        Args:
            None
        Returns:
            None
        """
        if RPI:
            self.clock = rtc.RTC()
            ### Initialize Modules
            if GPS:
                import adafruit_gps                         # GPS Module
                UART = busio.UART(tx=board.GP0, rx=board.GP1, baudrate=9600, timeout=10)
                gps_module = adafruit_gps.GPS(UART, debug=False)   # Use UART/pyserial
                # Turn on the basic GGA and RMC info (what you typically want)
                gps_module.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                # Set update rate to once a second (1hz) which is what you typically want.
                gps_module.send_command(b"PMTK220,1000")

                # # Wait until the GPS obtains a fix
                while not gps_module.has_fix:
                    print("Waiting for fix...")
                    gps_module.update() # This is needed, not exaclty sure why
                    time.sleep(1)

                # # Set RTC using Fix timestamp
                self.clock.datetime = time.struct_time((
                    gps_module.timestamp_utc.tm_year,
                    gps_module.timestamp_utc.tm_mon,
                    gps_module.timestamp_utc.tm_mday,
                    gps_module.timestamp_utc.tm_hour,
                    gps_module.timestamp_utc.tm_min,
                    gps_module.timestamp_utc.tm_sec,
                    0,
                    -1,
                    -1
                ))

                # Store GPS location
                # gps.latitude_degrees, gps.latitude_minutes
                # gps.longitude_degrees, gps.longitude_minutes
                # gps.fix_quality
                # gps.satellites
                # gps.altitude_m
                # gps.speed_knots
                self.gps_packet: str = f"STK:{self.timestamp()},{gps_module.latitude_degrees},{gps_module.longitude_degrees}"

                # Turn off GPS


            if LS:
                import sparkfun_qwiicas3935     # Lightning Module

                # Set up Interrupt pin on GPIO D21 with a pull-down resistor
                self.as3935_interrupt_pin = digitalio.DigitalInOut(board.GP8)
                self.as3935_interrupt_pin.direction = digitalio.Direction.INPUT
                self.as3935_interrupt_pin.pull = digitalio.Pull.DOWN

                # Create as3935 object
                i2c0 = busio.I2C(board.GP7, board.GP6)          # Create the first I2C interface
                self.as3935 = sparkfun_qwiicas3935.Sparkfun_QwiicAS3935_I2C(i2c0)

                # Check if connected
                if not self.as3935.connected:
                    print("Lightning Detector not connected. Please check wiring.")
                    sys.exit(1)

                # Set Mode
                self.as3935.indoor_outdoor = self.as3935.OUTDOOR
                afe_mode = self.as3935.indoor_outdoor
                if afe_mode == self.as3935.OUTDOOR:
                    print(f"{__name__}\t| The Lightning Detector is in the Outdoor mode.")
                elif afe_mode == self.as3935.INDOOR:
                    print(f"{__name__}\t| The Lightning Detector is in the Indoor mode.")
                else:
                    print(f"{__name__}\t| The Lightning Detector is in an Unknown mode.")

                # Callibrate - If these parameters should be changed, then do so in py
                self.as3935.noise_level = NOISE_FLOOR
                self.as3935.watchdog_threshold = WATCHDOG_THRESH
                self.as3935.spike_rejection = SPIKE_REJECT
            else:
                # Set up Interrupt pin on GPIO D21 with a pull-down resistor
                self.as3935_interrupt_pin = digitalio.DigitalInOut(board.GP8)
                self.as3935_interrupt_pin.direction = digitalio.Direction.INPUT
                self.as3935_interrupt_pin.pull = digitalio.Pull.DOWN


    def timestamp(self) -> str:
        """ Acquire current time from Real Time Clock Module

        Args:
            None
        Returns:
            time (str): current time
        """
        timestring = self.clock.datetime
        return timestring

    def lightning(self) -> str:
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
        distance = "disabled"
        intensity = "disabled"

        try:
            while True:
                # When the interrupt goes high
                if self.as3935_interrupt_pin.value:
                    if LS:
                        print("Interrupt:", end=" ")
                        interrupt_value = self.as3935.read_interrupt_register()

                        if interrupt_value == self.as3935.NOISE:
                            print("Noise.")
                            self.as3935.clear_statistics()
                        elif interrupt_value == self.as3935.DISTURBER:
                            print("Disturber.")
                            self.as3935.clear_statistics()
                        elif interrupt_value == self.as3935.LIGHTNING:
                            print("Lightning strike detected!")
                            # Distance estimation takes into account previous events.
                            print("Approximately: " + str(self.as3935.distance_to_storm) + "km away!")
                            distance = self.as3935.distance_to_storm
                            # Energy is a pure number with no physical meaning.
                            print("Energy: " + str(self.as3935.lightning_energy))
                            intensity = self.as3935.lightning_energy
                            self.as3935.clear_statistics()
                            break
                    else:
                        break
                    time.sleep(.5)
        except KeyboardInterrupt:
            pass

        ls_out = f"{distance},{intensity}"

        return ls_out
