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
import signal
import sys
import threading
import time
import datetime

import node

END = False         # Global Variable that kills threads
PACKET_QUEUE = []   # Sensor thread indicates when a package is ready

def handler(signum, frame) -> None:
    """This function will handle any system interrupts that we decide to use
    It relies on the "signal" python library (see documentation below)
    https://docs.python.org/3/library/signal.html

    TODO: Add more handling so that the errors can return more information

    Args:
        signum (int): number associated with interrupt
        frame (frame): = location that the interrupt came from
        signame (str): reads the name of the interrupt to the user
    Returns:
        None
    """
    signame = signal.Signals(signum).name
    print(f"{__name__}\t| Signal handler called with signal {signame} ({signum})")
    print(f"{__name__}\t| Frame = {frame}")

    # Handles a user input Ctrl + C
    if signame == "SIGINT":
        print(f"{__name__}\t|\tUser manually initiated shutdown using \"CTRL+C\"...")
        if node.CORES > 1:
            global END
            END = True
        else:
            sys.exit(0)

    # TODO: Handles a memory access conflict from two threads overlapping

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
        global END
        while not END:
            node.temp_check()
            PACKET_QUEUE.append(node.collect())
            if node.CORES == 1:
                END = True
        if node.CORES != 1:
            print(f"{__name__}\t| Thread 2 finished.")

    except ValueError as val_err:
        print(f"{__name__}\t| ISSUE WITH SENSORS! {val_err}")
        END = True

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
    global END
    while not END:
        # global PACKET_QUEUE
        if len(PACKET_QUEUE) > 0:
            node.send(PACKET_QUEUE.pop(0))
        elif node.CORES == 1:
            END = True
        time.sleep(1)
    if node.CORES != 1:
        print(f"{__name__}\t| Thread 1 finished.")
    END = True

def main():
    """
    Main function - will be run if this file is specified in terminal

    This will handle the two different threads
    """
    # System Settings
    print(f"{__name__}\t|\t* GPIO ENABLED...")
    node.gpio.setup()

    # Initial LoRa exchange
    # name = node.init()
    # node.setname(name)

    print(f"{__name__}\t| * Starting up device with %d Cores...")

    # Initialize Listener (for CTRL+C interrupts)
    signal.signal(signal.SIGINT, handler)

    try:
        # Setting up Threads based on core count
        if node.CORES <= 0:
            print(f"{__name__}\t| CORE COUNT MUST BE A POSITIVE INTEGER")

        elif node.CORES == 1:
            while True:
                global END
                sens_thread()
                END = False
                lora_thread()
                END = False

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
