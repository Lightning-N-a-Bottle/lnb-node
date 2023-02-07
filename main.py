"""
Main Module

- Documentation Notes:
    - https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
- TODO:
    - look into machine package - https://docs.micropython.org/en/latest/library/machine.html
    - sleep and wake from ls spi connection to save power
    - 
"""
import logging
import signal
import sys
import threading
import time

import node
from node import CORES, RPI, setname

END = False         # Global Variable that kills threads
PACKET_QUEUE = []   # Sensor thread indicates when a package is ready

def handler(signum, frame) -> None:
    """This function will handle any system interrupts that we decide to use
    It relies on the "signal" python library (see documentation below)
    https://docs.python.org/3/library/signal.html

    TODO: Add more handling so that the errors can return more information

    signum = number associated with interrupt
    frame = location that the interrupt came from
    signame = reads the name of the interrupt to the user
    """
    signame = signal.Signals(signum).name
    logging.error("Signal handler called with signal %s (%d)", signame, signum)
    logging.info("Frame = %s", frame)

    # Handles a user input Ctrl + C
    if signame == "SIGINT":
        logging.info("User manually initiated shutdown using \"CTRL+C\"...")
        if RPI:
            logging.info("Cleaning up GPIO Pins...")
            node.gpio.cleanup()
        if CORES > 1:
            global END
            END = True
        else:
            sys.exit(0)

    # TODO: Handles a memory access conflict from two threads overlapping


def thread1() -> None:
    """First Thread of the program, calls the "run" function of the LoRa Module.

    This method is kept simple to reduce the complexity of the main and to make testing modular.
    The loop relies on a global variable to determine when the threads should be killed.
    They have to be global because the threads are separate and asynchronous.
    """
    global END
    while not END:
        # global PACKET_QUEUE
        if len(PACKET_QUEUE) > 0:
            node.send(PACKET_QUEUE.pop(0))
        elif CORES == 1:
            END = True
        time.sleep(1)
    if CORES != 1:
        logging.info("Thread 1 finished.")
    # logging.error("ISSUE WITH LORA!")
    END = True

def thread2() -> None:
    """Second Thread of the program, calls the "run" function of the Sensor Module.

    This method is kept simple to reduce the complexity of the main and to make testing modular.
    The loop relies on a global variable to determine when the threads should be killed.
    They have to be global because the threads are separate and asynchronous.

    NOTE:   If we run this on the pico, this will have to be run on the main thread instead due to
            only having 2 cores
    """
    try:
        global END
        while not END:
            PACKET_QUEUE.append(node.collect())
            if CORES == 1:
                END = True
            time.sleep(1)
        if CORES != 1:
            logging.info("Thread 2 finished.")
    except ValueError as val_err:
        logging.error("ISSUE WITH SENSORS! %s", val_err)
        END = True

def main():
    """
    Main function - will be run if this file is specified in terminal

    This will handle the two different threads
    """
    # Initial Logger Settings
    fmt_main = "%(asctime)s | main\t\t: %(message)s"
    logging.basicConfig(format=fmt_main, level=logging.INFO,
                        datefmt="%Y-%m-%D %H:%M:%S")
    
    # System Settings
    if RPI:
        logging.info("* GPIO ENABLED...")
        node.gpio.setup()
    else:
        logging.info("* GPIO DISABLED...")

    # Initial LoRa exchange
    name = node.init()
    node.setname(name)

    logging.info("* Starting up device with %d Cores...", CORES)

    # Initialize Listener (for CTRL+C interrupts)
    signal.signal(signal.SIGINT, handler)

    try:
        # Setting up Threads based on core count
        if CORES <= 0:
            logging.error("CORE COUNT MUST BE A POSITIVE INTEGER")
        elif CORES == 1:
            while True:
                global END
                thread2()
                END = False
                thread1()
                END = False
                node.temp_check()
        elif CORES == 2:    # TODO: Test whether this actually uses two cores, or if the handler uses a third
            t1 = threading.Thread(target=thread2)
            t1.start()
            logging.info("Threads Launched...")
            thread1()       # This is a blocking function call, so anything after this won't run until END
            node.temp_check()
            
            # Safely closing all threads
            t1.join()
        else:
            t1 = threading.Thread(target=thread1)
            t2 = threading.Thread(target=thread2)
            t1.start()
            t2.start()
            logging.info("Threads Launched...")

            while True: # Because the other threads are not blocking, this will block until CTRL+C
                node.temp_check()
                time.sleep(5)
                if END:
                    break
            # Safely closing all threads
            t1.join()
            t2.join()
        logging.info("All Threads finished...exiting")
    except ValueError as val_err:       # TODO: Handle other error types better
        return str(val_err)

if __name__ == "__main__":
    sys.exit(main())
