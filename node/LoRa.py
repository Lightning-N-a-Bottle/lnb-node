"""
LoRa Thread Main
"""
import logging

from .gpio import gps, lora_rx, lora_tx


def init() -> str:
    """
    Initializes the Lora connection
    """
    packet = gps()
    send(packet)        # Send GPS data to Raspberry Pi
    # name = receive()    # Receives new name from the Raspberry Pi FIXME: not blocking
    name = "name"       # TODO: Remove Later
    return name

def receive() -> str:
    """
    Listen for incoming LoRa packets
    This should hypothetically be the default state
    """
    pack = ""           # TODO: cleanup
    while pack == "":
        pack = lora_rx()
    return pack

def send(packet: str) -> int:
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

    # Debug packet
    if "PACK:" in packet:
        logging.info("\t__name__=%s\t|\tpacket=%s\n", __name__, packet)
    else:
        logging.info("* GPS NMEA Data\t=\t%s", packet)

    # Send Packet
    lora_tx(packet)


    return 0
