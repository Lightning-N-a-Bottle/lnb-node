"""
Main Module
"""
import _thread

import LoRa
import sensor


def main():
    """
    Main function

    This will handle the two different threads
    """

    print("Hello World!")

    _thread.start_new_thread(sensor.thread, ())
    LoRa.thread()
    _thread.exit()

if __name__ == "__main__":
    main()
