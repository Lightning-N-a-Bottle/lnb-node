"""
LoRa Thread Main
"""
import time
import logging


def run(PACKET) -> int:
    """
    This thread will process all LoRa communications

    TODO: LoRa Flowchart

    TODO: Implement RX
    TODO: Implement TX
    TODO: Add ability to detect new packets to send
    TODO: Add LoRa setup process
    """
    format = "%(asctime)s | LoRa\t\t: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info(f"\t{__name__=}\t\t| {PACKET=}\n")

if __name__ == "__main__":
    ### Main Block for LoRa - this will only be run if using LoRa individually
    # Configuring startup settings
    format = "%(asctime)s | LoRa\t\t: %(message)s "
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Starting up device...")

    PACKET = "12:34:56,1,1"
    result = run(PACKET)
    logging.info(f"\"run()\" function returned with code {result}")
