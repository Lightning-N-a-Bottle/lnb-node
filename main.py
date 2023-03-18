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
import logging
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
    logging.error("\t%s\t|\tSignal handler called with signal %s (%d)", __name__, signame, signum)
    logging.info("\t%s\t|\tFrame = %s", __name__, frame)

    # Handles a user input Ctrl + C
    if signame == "SIGINT":
        logging.info("\t%s\t|\tUser manually initiated shutdown using \"CTRL+C\"...", __name__)
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
            logging.info("\t%s\t|\tThread 2 finished.", __name__)
    except ValueError as val_err:
        logging.error("\t%s\t|\tISSUE WITH SENSORS! %s", __name__, val_err)
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
        logging.info("\t%s\t|\tThread 1 finished.", __name__)
    # logging.error("\t%s\t|\tISSUE WITH LORA!", __name__)
    END = True

def main():
    """
    Main function - will be run if this file is specified in terminal

    This will handle the two different threads
    """
    # Initial Logger Settings
    fmt_main = "%(asctime)s | %(message)s"
    filename = datetime.datetime.now().strftime("./logs/debug_%Y-%m-%d_%H-%M-%S.log")

    # logger = logging.getLogger(__name__)
    
    # # Create handlers
    # c_handler = logging.StreamHandler()
    # f_handler = logging.FileHandler(filename)
    # c_handler.setLevel(logging.INFO)
    # f_handler.setLevel(logging.INFO)

    # # Create formatters and add it to handlers
    # c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    # f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # c_handler.setFormatter(c_format)
    # f_handler.setFormatter(f_format)

    # # Add handlers to the logger
    # logger.addHandler(c_handler)
    # logger.addHandler(f_handler)
    if node.OUTFILE:
        logging.basicConfig(filename=filename, format=fmt_main,
                        level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
    else:
        logging.basicConfig(format=fmt_main, level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")


    # System Settings
    if node.RPI:
        logging.info("\t%s\t|\t* GPIO ENABLED...", __name__)
        node.gpio.setup()
    else:
        logging.info("\t%s\t|\t* GPIO DISABLED...", __name__)

    # Initial LoRa exchange
    name = node.init()
    node.setname(name)

    logging.info("\t%s\t|\t* Starting up device with %d Cores...", __name__, node.CORES)

    # Initialize Listener (for CTRL+C interrupts)
    signal.signal(signal.SIGINT, handler)

    try:
        # Setting up Threads based on core count
        if node.CORES <= 0:
            logging.error("\t%s\t|\tCORE COUNT MUST BE A POSITIVE INTEGER", __name__)
        elif node.CORES == 1:
            while True:
                global END
                sens_thread()
                END = False
                lora_thread()
                END = False
        elif node.CORES == 2:    # TODO: Test whether this actually uses two cores, or if the handler uses a third
            t1 = threading.Thread(target=sens_thread)
            t1.start()
            logging.info("\t%s\t|\tThreads Launched...\n", __name__)
            lora_thread()       # This is a blocking function call until END is set True

            # Safely closing all threads
            t1.join()
        else:
            t1 = threading.Thread(target=lora_thread)
            t2 = threading.Thread(target=sens_thread)
            t1.start()
            t2.start()
            logging.info("\t%s\t|\tThreads Launched...\n", __name__)

            while True: # Because the other threads are not blocking, this will block until CTRL+C
                if END:
                    break
            # Safely closing all threads
            t1.join()
            t2.join()
        # System Settings
        if node.RPI:
            node.gpio.cleanup()
        logging.info("\t%s\t|\tAll Threads finished...exiting", __name__)
    except ValueError as val_err:       # TODO: Handle other error types better
        return str(val_err)

if __name__ == "__main__":
    sys.exit(main())
