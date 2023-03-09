""" constants.py
Stores all constant variables that are shared throughout the module

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
Constants Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1constants.html
"""
import os
import platform

PICO = False        # Running on PICO

### IDENTIFY SYSTEM CORE COUNT ###
CORES = os.cpu_count()
CORES = 2

### IDENTIFY SYSTEM OS/GPIO CAPABILITY ###
RPI = False
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
