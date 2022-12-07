"""
LoRa Thread Main
"""
import time
import logging


def run() -> None:
    """
    This thread will process all LoRa communications

    TODO: LoRa Flowchart

    TODO: Implement RX
    TODO: Implement TX
    TODO: Add ability to detect new packets to send
    TODO: Add LoRa setup process
    """
    logging.info("LoRa")
    time.sleep(1)

if __name__ == "__main__":
    """
    Main Block for LoRa - this will only be run if using LoRa individually
    """