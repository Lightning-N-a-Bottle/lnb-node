"""
Main Module

- Documentation Notes:
    - https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

"""
import logging
import platform
import signal
import sys
import threading
import time

import src

if platform.system() == "Linux":
    if platform.release().find('raspi'):
        print("THIS IS A RASPBIAN SYSTEM\n")
    else:
        print("THIS IS A LINUX SYSTEM\n")
elif platform.system() == "Windows":
    print("THIS IS A WINDOWS SYSTEM\n")
else:
    print("I DON'T KNOW WHAT SYSTEM THIS IS\n")


# from loguru import logger
# import multiprocessing as mp


END = False # Global Variable that kills threads
PACKET_QUEUE = [] # Sensor thread indicates when a package is ready

def handler(signum, frame) -> None:
    """
    This function will handle any system interrupts that we decide to use
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
        global END
        END = True

    # TODO: Handles a memory access conflict from two threads overlapping


def thread1() -> None:
    """First Thread of the program, calls the "run" function of the LoRa Module.

    This method is kept simple to reduce the complexity of the main and to make testing modular.
    The loop relies on a global variable to determine when the threads should be killed.
    They have to be global because the threads are separate and asynchronous.
    """


    # global END
    while not END:
        # global PACKET_QUEUE
        if len(PACKET_QUEUE) > 0:
            src.send(PACKET_QUEUE.pop(0))
        time.sleep(1)
    logging.info("Thread 1 finished.")

def thread2() -> None:
    """Second Thread of the program, calls the "run" function of the Sensor Module.

    This method is kept simple to reduce the complexity of the main and to make testing modular.
    The loop relies on a global variable to determine when the threads should be killed.
    They have to be global because the threads are separate and asynchronous.

    NOTE:   If we run this on the pico, this will have to be run on the main thread instead due to
            only having 2 cores
    """
    # global END
    while not END:
        PACKET_QUEUE.append(src.collect())
        time.sleep(1)
    logging.info("Thread 2 finished.")

def main():
    """
    Main function - will be run if this file is specified in terminal

    This will handle the two different threads
    """
    try:
        # Configuring startup settings
        fmt_main = "%(asctime)s | main\t\t: %(message)s"
        logging.basicConfig(format=fmt_main, level=logging.INFO,
                            datefmt="%Y-%m-%D %H:%M:%S")
        logging.info("Starting up device...")
        # logger.info("Main      : Starting up device...")
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
            if END:
                break

        t1.join()
        t2.join()
        logging.info("All Threads finished...exiting")
    except ValueError as val_err:
        return str(val_err)

if __name__ == "__main__":
    sys.exit(main())
    # with logger.catch():
    #     main()