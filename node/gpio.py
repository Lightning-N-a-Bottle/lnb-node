"""
gpio interface

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
GPIO Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1gpio.html
"""
import sys
import time

from .constants import (
    RPI,
    GPS,
    LS,
    NOISE_FLOOR,
    WATCHDOG_THRESH,
    SPIKE_REJECT,
)  # , LORA, FREQ, TX_POW

# import RPi.GPIO as GPIO
import board
import busio
import digitalio
import rtc


class Devices:
    """ Class to interact with all modules """
    def __init__(self) -> None:
        """Initializes RPI GPIO pins

        Args:
            None
        Returns:
            None
        """
        if RPI:
            self.clock = rtc.RTC()

            ### Initialize Modules
            GPS_ENABLE = digitalio.DigitalInOut(board.GP3)
            GPS_ENABLE.direction = digitalio.Direction.OUTPUT

            if GPS:
                import adafruit_gps # GPS Module
                # Enable GPS for collection
                GPS_ENABLE.value = 1

                UART = busio.UART(tx=board.GP0, rx=board.GP1, baudrate=9600, timeout=10)
                gps_module = adafruit_gps.GPS(UART, debug=False)    # Use UART/pyserial

                # Turn on the basic GGA and RMC info (what you typically want)
                gps_module.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
                # Set update rate to once a second (1hz) which is what you typically want.
                gps_module.send_command(b"PMTK220,1000")

                # Wait until the GPS obtains a fix
                while not gps_module.has_fix:
                    print("Waiting for fix...")
                    gps_module.update()     # Refreshes "has_fix" value
                    time.sleep(1)
                print("Got GPS Fix!")

                # Set RTC using Fix timestamp
                self.clock.datetime = time.struct_time(
                    (
                        gps_module.timestamp_utc.tm_year,
                        gps_module.timestamp_utc.tm_mon,
                        gps_module.timestamp_utc.tm_mday,
                        gps_module.timestamp_utc.tm_hour,
                        gps_module.timestamp_utc.tm_min,
                        gps_module.timestamp_utc.tm_sec,
                        0,
                        -1,
                        -1,
                    )
                )

                # Store GPS location
                # gps.latitude_degrees, gps.latitude_minutes
                # gps.longitude_degrees, gps.longitude_minutes
                # gps.fix_quality
                # gps.satellites
                # gps.altitude_m
                # gps.speed_knots
                self.gps_lat_long = f"{gps_module.latitude_degrees},{gps_module.longitude_degrees}"

            else:
                self.gps_lat_long = "-1,-1"

            # Turn off GPS Module after Fix or if disabled in constants.py
            GPS_ENABLE.value = 0

            if LS:
                import sparkfun_qwiicas3935  # Lightning Module

                # Set up Interrupt pin on GPIO D21 with a pull-down resistor
                self.as3935_interrupt_pin = digitalio.DigitalInOut(board.GP8)
                self.as3935_interrupt_pin.direction = digitalio.Direction.INPUT
                self.as3935_interrupt_pin.pull = digitalio.Pull.DOWN
                
                # On board LED for lightning detection
                self.PiLED = digitalio.DigitalInOut(board.LED)
                self.PiLED.direction = digitalio.Direction.OUTPUT

                # Create as3935 object
                i2c0 = busio.I2C(board.GP7, board.GP6)  # Create the first I2C interface
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

            i = 0
            while True:

                # When the interrupt goes high
                if self.as3935_interrupt_pin.value:
                    if LS:

                        print("Interrupt:", end=" ")
                        interrupt_value = self.as3935.read_interrupt_register()

                        # Distance estimation takes into account previous events.
                        distance = self.as3935.distance_to_storm
                        # Energy is a pure number with no physical meaning.
                        intensity = self.as3935.lightning_energy

                        print("Energy: " + str(distance))
                        intensity = self.as3935.lightning_energy

                        if interrupt_value == self.as3935.NOISE:
                            print("Noise.")
                            self.as3935.clear_statistics()
                        elif interrupt_value == self.as3935.DISTURBER:
                            i += 1
                            print(f"Disturber {i} detected {distance}km away!")
                            self.as3935.clear_statistics()
                            # Comment out break to not save to csv
                            break
                        elif interrupt_value == self.as3935.LIGHTNING:
                            print(f"Lightning strike detected {distance}km away!")
                            print(f"Energy: {intensity}")
                            #Turn on PiLED
                            self.PiLED.value = 1
                            self.as3935.clear_statistics()
                            break

                    else:
                        break
                    time.sleep(0.5)
                    self.PiLED.value = 0
        except KeyboardInterrupt:
            pass

        ls_out = f"{distance},{intensity}"

        return ls_out
