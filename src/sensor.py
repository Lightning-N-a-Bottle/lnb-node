"""
Sensor Thread Main
"""
import time
import logging


def run() -> None:
    """
    This thread will handle all communications with the sensors and create new packets

    TODO: Sensor Flowchart

    TODO: RTC interface
    TODO: Lightning sensor interface
    TODO: Packet creating
    FIXME: Does GPS go here or with LoRa?
    """
    logging.info("Sensor")
    time.sleep(1)

if __name__ == "__main__":
    """
    Main Block for Sensors - this will only be run if using Sensors individually
    """