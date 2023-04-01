""" constants.py
Stores all constant variables that are shared throughout the module

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
Constants Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1constants.html
"""
import os
MPY = False         # Running MicroPython
CORES = 1
RPI = False
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

### WHAT MODULES ARE CURRENTLY CONNECTED ###
LS = True          # Lightning Sensor
RTC = True         # Real Time Clock
GPS = True         # GPS Location
CARD = True        # SD Card Module

### DEV PARAMETERS ###
OUTFILE = False     # Set True to print to file, False to console

# LORA
FREQ = 915.0        # MHz - Frequency channel for LoRa
TX_POW = 23         # Transmit Power

# AS3935
NOISE_FLOOR = 5     # (1-7, default=2) Lower to detect smaller strikes, at the cost of more noise
WATCHDOG_THRESH = 2 # (1-10, default=2) TODO:
SPIKE_REJECT = 1

# (1-11, default=2) Modify the shape of spikes, round at the cost of range
