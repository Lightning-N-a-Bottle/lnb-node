"""
LoRa Thread Main
"""
import logging
from .gpio import gps

def init() -> str:
    packet = gps()
    send(packet)        # Send GPS data to Raspberry Pi
    name = receive()    # Receives new name from the Raspberry Pi
    logging.info("This Node is now named: %s", name)
    return name

def receive() -> str:
    return "testname"

def send(packet) -> int:
    """
    This thread will process all LoRa communications

    TODO: LoRa Flowchart

    TODO: Implement RX
    TODO: Implement TX
    TODO: Add ability to detect new packets to send
    TODO: Add LoRa setup process
    """
    fmt_lora = "%(asctime)s | LoRa\t\t: %(message)s"
    logging.basicConfig(format=fmt_lora, level=logging.INFO,
                        datefmt="%H:%M:%S")
    if "PACK:" in packet:
        logging.info("\t__name__=%s\t|\tpacket=%s\n", __name__, packet)



    return 0
