"""
LoRa Thread Main
"""
import logging

from .gpio import gps, lora_rx, lora_tx


def init() -> str:
    """ Initializes the Lora connection

    This will acquire the GPS location and attempt to send it to the server
    If successful, the server will respond with a string, which will become the reference
    name for the local node.
    Afterwards the GPS module should be shut down.

    Args:
        None
    Returns:
        None
    """

    packet = gps()
    send(packet)        # Send GPS data to Raspberry Pi
    # name = receive()    # Receives new name from the Raspberry Pi FIXME: not blocking
    name = "name"       # TODO: Remove Later
    return name

def receive() -> str:
    """ Listen for incoming LoRa packets

    This should hypothetically be the default state

    Args:
        None
    Returns:
        pack (str): The packet received over LoRa
    """
    pack = ""           # TODO: cleanup
    while pack == "":
        pack = lora_rx()
    return pack

def send(packet: str) -> None:
    """
    This thread will process all LoRa communications
    
    Args:
        packet (str): The compiled string that will be sent over LoRa
    Returns:
        None
    
    TODO: Should the return type be none, or should it wait for confirmation?
    """
    # Debug packet
    if "PACK:" in packet:
        logging.info("\t__name__=%s\t|\tpacket=%s\n", __name__, packet)
    else:
        logging.info("* GPS NMEA Data\t=\t%s", packet)

    # Send Packet
    lora_tx(packet)
