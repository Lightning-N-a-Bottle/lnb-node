""" @file       constants.py
    @author     Sean Duffie
    @brief      Stores all constant variables that are shared throughout the module

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
Constants Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1constants.html
"""
import os

MPY: bool = False   # Running MicroPython
CORES: int = 1      # System Core Count (For multithreading)
RPI: bool = False   # Running on a Raspberry Pi
try:
    if os.uname().sysname == "rp2040":
        print("Running on a Pico!")
    MPY = True
    RPI = True
except AttributeError:
    import platform

    ### IDENTIFY SYSTEM CORE COUNT ###
    # CORES = os.cpu_count()
    ### IDENTIFY SYSTEM OS/GPIO CAPABILITY ###
    if platform.system() == "Linux" and platform.release().find('raspi'):
        RPI = True

### MODULE NAME (FOR FILE SORTING) ###
NAME: str = "NODE-A"

### WHAT MODULES ARE CURRENTLY CONNECTED ###
LS: bool = True         # Lightning Sensor
GPS: bool = True        # GPS Module
CARD: bool = True       # SD Card Module
RTC: bool = False       # Real Time Clock [True for external, False for internal] *not currently used

### DEV PARAMETERS ###
# AS3935
NOISE_FLOOR: int = 5        # (1-7, default=2) Lower to detect smaller strikes, with more noise
WATCHDOG_THRESH: int = 2    # (1-10, default=2) TODO:
SPIKE_REJECT: int = 1       # (1-11, default=2) Modify the shape of spikes, round with lower range
TUNE_CAP: int = 0           # (0-120, default=0) Modify the tune capacitor 