"""
Sensor Thread
This file in the module will handle the packaging of sensor data
It will be responsible for the GPIO interface with sensor equipment
"""
import logging

from .gpio import lightning, rtc


def collect(name) -> str:
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

    # When lightning is detected, this will populate the string with the sensor data
    lng = lightning()       # Acquire Lightning Distance/Intensity

    # Acquire RTC Timestamp
    tstmp = rtc()

    # Append to PACKET_QUEUE
    packet = f"PACK:{name},{tstmp},{lng}"
    logging.info("\t__name__=%s\t|\tpacket=%s", __name__, packet)

    return packet
