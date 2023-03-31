# Write your code here :-)
import os

import board
import busio
import sdcardio
import storage


spi = busio.SPI(board.GP18, board.GP16, board.GP19)
cs = digitalio.DigitalInOut(board.GP17)


sd = sdcardio.SDCard(spi, cs)

vfs = storage.VfsFat(sd)

storage.mount(vfs, '/sd')
os.listdir('/sd')
# Setup
file = open("/sd/lightning.csv", "w")
file.write('Lightning Distance, Intensisty, Lat, Long\n') # Headers
file.close()

# Append as needed
file = open("/sd/lightning.csv", "a")
file.write(packet)
file.close()

