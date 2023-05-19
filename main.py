""" @file       code.py
    @author     Sean Duffie
    @brief      Main Module
    @details    Launches all tasks, would be responsible for threading if implemented

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html

Documentation Notes:
    - https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    - https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files
    - https://www.tutorialspoint.com/python/python_multithreading.htm
TODO:
    - implement threading in circuitpython (if available)
    - sleep and wake from ls spi connection to save power (probably not needed)
"""
import sys

import node

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

def sdcard_thread() -> None:
    """First Thread of the program, calls the "run" function of the SD Card Module.

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
    global reader, card
    reader = node.Sensor()
    card = node.Storage()

    # Name the csv output file for the current session. Comment out to use "local" for default
    card.set_filename(reader.get_filename())

    print(f"{__name__}\t| * Starting up device with {node.CORES} Cores...")

    try:
        # Setting up Threads based on core count
        if node.CORES <= 0:
            print(f"{__name__}\t| CORE COUNT MUST BE A POSITIVE INTEGER")

        elif node.CORES == 1:
            while True:
                sens_thread()
                sdcard_thread()

        else:
            # t1 = threading.Thread(target=sens_thread)
            # t1.start()
            print(f"{__name__}\t|\tThreads Launched...\n")
            # sdcard_thread()       # This is a blocking function call until END is set True

            # Safely closing all threads
            # t1.join()

        # System Settings
        print(f"{__name__}\t|\tAll Threads finished...exiting")

    except ValueError as val_err:       # TODO: Handle other error types better
        return str(val_err)

if __name__ == "__main__":
    sys.exit(main())
