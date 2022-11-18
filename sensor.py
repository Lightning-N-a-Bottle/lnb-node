"""
Sensor Thread Main
"""
import time


def thread() -> None:
    """
    This thread will handle all communications with the sensors and create new packets
    TODO: RTC interface
    TODO: Lightning sensor interface
    TODO: Packet creating
    FIXME: Does GPS go here or with LoRa?
    """
    while True:
        print("Sensor")
        time.sleep(1)
