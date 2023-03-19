""" constants.py
Stores all constant variables that are shared throughout the module

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
Constants Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1constants.html
"""
import os
MPY = False         # Running MicroPython
CORES = 2
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
LS = False          # Lightning Sensor
RTC = False         # Real Time Clock
GPS = False         # GPS Location
LORA = True         # LoRa Radio

### DEV PARAMETERS ###
OUTFILE = False     # Set True to print to file, False to console
FREQ = 915.0        # MHz - Frequency channel for LoRa
