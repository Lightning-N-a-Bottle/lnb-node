"""
constants.py
Stores all constant variables that are shared throughout the module
"""
import platform
import os

### IDENTIFY SYSTEM CORE COUNT ###
CORES = os.cpu_count()

### IDENTIFY SYSTEM OS/GPIO CAPABILITY ###
RPI = False
if platform.system() == "Linux" and platform.release().find('raspi'):
    RPI = True
