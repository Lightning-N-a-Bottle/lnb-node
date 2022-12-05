"""
Main Module
"""
import threading

import LoRa
import sensor

stopflag = False

def main():
    """
    Main function

    This will handle the two different threads
    """

    print("Hello World!")

    t1 = LoRa("LoRa")
    print("LoRa Thread: ")
    t1.start()
    sensor.thread()

    print("threads finished...exiting")
    stopflag = True
    t1.join()
    print("Done.")

if __name__ == "__main__":
    main()
