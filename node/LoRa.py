""" LoRa.py
LoRa Thread Main

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
LoRa Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1_lo_ra.html
"""
# from .gpio import lora_tx
# from .constants import MPY
import os
import busio
import board
import digitalio
import sdcardio
import storage

# Set up GPIO for SD Card
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
cs = board.GP17

# Create the SD object
sd = sdcardio.SDCard(spi, cs)

# Format the storage
vfs = storage.VfsFat(sd)

# Mount the drive and call id /sd
storage.mount(vfs, '/sd')

# list all files in the drive
os.listdir('/sd')

def send(packet: str) -> None:
    """ Processes Main LoRa communications with packet transfer



    Args:
        packet (str): The compiled string that will be sent over LoRa
    Returns:
        None

    TODO: Should the return type be none, or should it wait for confirmation?
    """
    # Debug packet
    # if "PACK:" in packet:
    # logging.info("\t%s\t|\tpacket=%s\n", __name__, packet)
    # else:

    # Send Packet
    # lora_tx(packet)

    print(f"{__name__}\t|\tDELIVERED={packet}")
    # Append as needed
    # Open the file on the sd card to save the lightning data and sent to append "a"
    file = open("/sd/lightning.csv", "a")

    # write the "packet" to the file
    file.write(packet+"\n") # need an escape character for csv

    # close the file
    file.close()

    # else:
        # logging.error("\t%s\t|\tResponse was different...", __name__)

# TimeStamp,Distance,gps lat, gps long