""" code.py
    This file is meant to help us organize our port to RPi Pico
    The Raspberry Pi Pico should be able to port 
    However, we need a more efficient way to integrate and test code while debugging
    So, this file will simply choose which main file to run

    To use this, import the main function from your chosen file and comment out the others
"""
from main import main
# from lsens import main
# from gps import main

if __name__ == "__main__":
    main()
