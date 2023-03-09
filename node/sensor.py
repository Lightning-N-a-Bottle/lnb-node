""" sensor.py
Sensor Thread
This file in the module will handle the packaging of sensor data
It will be responsible for the GPIO interface with sensor equipment

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
LoRa Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1sensor.html
"""
import logging

from .gpio import lightning, rtc

NAME = ""

def setname(name: str) -> None:
    """ Modifies name identifier of current node

    The purpose for having the name is to reduce power consumption from the GPS.
    By only acquiring the GPS data on startup, the GPS can be turned off after first measurement.
    The node still must distinguish itself from other nodes, so the server will assign a name.

    Args:
        name (str): name assigned to node by server
    Returns:
        None
    """
    # Global
    global NAME
    NAME = name
    logging.info("\t%s\t|\t* This Node is now named:\t%s", __name__, NAME)


def collect() -> str:
    """ Collects data from sensors and compiles it into a string

    This thread will handle all communications with the sensors and create new packets

    Args:
        None
    Returns:
        packet (str): The properly formatted packet to be passed to LoRa
    """
    # When lightning is detected, this will populate the string with the sensor data
    lng: str = lightning()       # Acquire Lightning Distance/Intensity

    # Acquire RTC Timestamp
    tstmp: str = rtc()

    # Append to PACKET_QUEUE
    packet: str = f"STK:{NAME},{tstmp},{lng}"
    logging.info("\t%s\t|\tCREATED=%s", __name__, packet)

    return packet
