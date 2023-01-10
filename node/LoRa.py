"""
LoRa Thread Main
"""
import logging

from .constants import RPI
if RPI:
    # Configure LoRa Radio
    # CS =  # arbitrary - control select
    # RST =  #arbitrary - reset
    # spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    # rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    # rfm9x.tx_power = 23
    prev_packet = None

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
    logging.info("\t__name__=%s\t|\tpacket=%s\n", __name__, packet)

    if RPI:
        packet_data = bytes(packet)
        rfm9x.send(packet_data)

    return 0
