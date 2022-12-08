"""
Main Module

- Documentation Notes:
    - https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

"""
import signal
import logging
import threading
# import multiprocessing as mp
import time

import LoRa
import sensor


threads = True # Global Variable that kills threads

def handler(signum, frame) -> None:
    """
    This function will handle any system interrupts that we decide to use
    It relies on the "signal" python library (see documentation below)
    https://docs.python.org/3/library/signal.html

    signum = number associated with interrupt
    frame = location that the interrupt came from
    signame = reads the name of the interrupt to the user
    """
    signame = signal.Signals(signum).name
    print(f'Signal handler called with signal {signame} ({signum})')

    # Handles a user input Ctrl + C
    if signame == "SIGINT":
        logging.info("Shutting down...")
        global threads
        threads = False


def thread1() -> None:
    """First Thread of the program, calls the "run" function of the LoRa Module.

    This method is kept simple to reduce the complexity of the main and to make testing modular.
    The loop relies on a global variable to determine when the threads should be killed.
    They have to be global because the threads are separate and asynchronous.
    """
    global threads
    while threads:
        LoRa.run()
    logging.info("Thread 1 finished.")

def thread2() -> None:
    """Second Thread of the program, calls the "run" function of the Sensor Module.
    
    This method is kept simple to reduce the complexity of the main and to make testing modular.
    The loop relies on a global variable to determine when the threads should be killed.
    They have to be global because the threads are separate and asynchronous.

    NOTE:   If we run this on the pico, this will have to be run on the main thread instead due to
            only having 2 cores
    """
    global threads
    while threads:
        sensor.run()
    logging.info("Thread 2 finished.")


if __name__ == "__main__":
    """
    Main function - will be run if this file is specified in terminal

    This will handle the two different threads
    """
    # Configuring startup settings
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.info("Main      : Starting up device...")
    signal.signal(signal.SIGINT, handler)

    # Setting up Threads
    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)
    # t1 = mp.Process(target=thread1)
    # t2 = mp.Process(target=thread2)
    t1.start()
    t2.start()
    logging.info("Threads Launched...")

    # Safely closing all threads
    while True:
        if not threads:
            break

    t1.join()
    t2.join()
    logging.info("All Threads finished...exiting")
