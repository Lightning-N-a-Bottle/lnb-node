""" constants.py
Stores all constant variables that are shared throughout the module

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
Constants Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1constants.html
"""
import os
import platform

### IDENTIFY SYSTEM CORE COUNT ###
CORES = 2#os.cpu_count()

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
FREQ = 915.0        # MHz - Frequency channel for LoRa