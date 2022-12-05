"""
Sensor Thread Main
"""
# import signal
import time

# import LoRa


def thread() -> None:
    """
    This thread will handle all communications with the sensors and create new packets
    TODO: RTC interface
    TODO: Lightning sensor interface
    TODO: Packet creating
    FIXME: Does GPS go here or with LoRa?
    """
    # signal.signal(signal.SIGINT, LoRa.shutdown)  # type: ignore

    try:
        while True:
            print("Sensor")
            time.sleep(1)
    finally:
        print("Shutting down")
        return