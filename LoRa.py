"""
LoRa Thread Main
"""
import time


def thread() -> None:
    """
    This thread will process all LoRa communications
    TODO: Implement RX
    TODO: Implement TX
    TODO: Add ability to kill thread
    TODO: Add ability to detect new packets to send
    TODO: Add LoRa setup process
    """
    while True:
        print("LoRa")
        time.sleep(1)
        