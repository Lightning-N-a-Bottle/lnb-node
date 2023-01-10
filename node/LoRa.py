"""
LoRa Thread Main
"""
import logging
from .constants import RPI

if RPI is True:         # TODO: Maybe add an additional file for GPIO operations?
    ### DEFINE GPIO PINS ###
    import RPi.GPIO as GPIO     # GPIO
    import adafruit_rfm9x       # LoRa
    GPIO.setmode(GPIO.board)
    ## GPIO.setup
    ## GPIO.output
    
    # Configure LoRa Radio
    # CS =  # arbitrary - control select
    # RST =  #arbitrary - reset
    # spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    # rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    # rfm9x.tx_power = 23
    # prev_packet = None


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

if __name__ == "__main__":
    ### Main Block for LoRa - this will only be run if using LoRa individually
    # Configuring startup settings
    FMT = "%(asctime)s | LoRa\t\t: %(message)s "
    logging.basicConfig(format=FMT, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Starting up device...")

    PACKET = "12:34:56,1,1"
    logging.info("\"send()\" function returned with code %s", send(PACKET))
