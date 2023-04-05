""" code.py
Main Module

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html

Documentation Notes:
    - https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    - https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files
    - https://www.tutorialspoint.com/python/python_multithreading.htm
TODO:
    - look into machine package - https://docs.micropython.org/en/latest/library/machine.html
    - sleep and wake from ls spi connection to save power
    - 
"""
import sys

import node

END = False         # Global Variable that kills threads
PACKET_QUEUE = []   # Sensor thread indicates when a package is ready

def sens_thread() -> None:
    """Second Thread of the program, calls the "run" function of the Sensor Module.

    This method is kept simple to reduce the complexity of the main and to make testing modular.
    The loop relies on a global variable to determine when the threads should be killed.
    They have to be global because the threads are separate and asynchronous.

    Args:
        None
    Returns:
        None

    NOTE:   If we run this on the pico, this will have to be run on the main thread instead due to
            only having 2 cores
    """
    try:
        PACKET_QUEUE.append(reader.collect())

    except ValueError as val_err:
        print(f"{__name__}\t| ISSUE WITH SENSORS! {val_err}")

def lora_thread() -> None:
    """First Thread of the program, calls the "run" function of the LoRa Module.

    This method is kept simple to reduce the complexity of the main and to make testing modular.
    The loop relies on a global variable to determine when the threads should be killed.
    They have to be global because the threads are separate and asynchronous.

    Args:
        None
    Returns:
        None
    """
    if len(PACKET_QUEUE) > 0:
        card.save(PACKET_QUEUE.pop(0))

def main():
    """
    Main function - will be run if this file is specified in terminal

    This will handle the two different threads
    """
    # System Settings
    print(f"{__name__}\t|\t* GPIO ENABLED...")
    global devices, reader, card
    devices = node.Devices()
    reader = node.Sensor(devices=devices)
    card = node.Storage()

    print(f"{__name__}\t| * Starting up device with %d Cores...")

    try:
        # Setting up Threads based on core count
        if node.CORES <= 0:
            print(f"{__name__}\t| CORE COUNT MUST BE A POSITIVE INTEGER")

        elif node.CORES == 1:
            while True:
                sens_thread()
                lora_thread()

        else:
            t1 = threading.Thread(target=sens_thread)
            t1.start()
            print(f"{__name__}\t|\tThreads Launched...\n")
            lora_thread()       # This is a blocking function call until END is set True

            # Safely closing all threads
            t1.join()

        # System Settings
        node.gpio.cleanup()
        print(f"{__name__}\t|\tAll Threads finished...exiting")

    except ValueError as val_err:       # TODO: Handle other error types better
        return str(val_err)

if __name__ == "__main__":
    sys.exit(main())
