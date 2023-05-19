""" @file       code.py
    @author     Sean Duffie
    @brief      This file simply selects the desired main file to be run
    @details    The Raspberry Pi Pico will always run the code.py file on startup, however -
                because git doesn't handle renaming easily, we need a different way to swap mains
                without renaming files.

                To use this, import the main function from your chosen file and comment out the others
"""
from main import main
# from lsens import main
# from gps import main

if __name__ == "__main__":
    main()
