"""
Main Module
"""
import _thread
import time


def second_thread():
    """
    Runs on the Second Core
    """
    while True:
        print("Second thread")
        time.sleep(1)

def main():
    """
    Main function

    This will handle the two different threads
    """
    print("Hello World!")

    _thread.start_new_thread(second_thread, ())

    while True:
        print("Main")
        time.sleep(2)

if __name__ == "__main__":
    main()
