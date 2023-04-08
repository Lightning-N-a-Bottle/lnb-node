""" LoRa.py
LoRa Thread Main

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
LoRa Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1_lo_ra.html
"""
import os

# Circuitpython imports
import board
import busio
import sdcardio
import storage

# Module Constants
from .constants import CARD

class Storage:
    """ Class set  """
    def __init__(self):
        """ Initial setup for the SD Card
        
            This will create an SD Card object, format it, then mount it to the filesystem
            Afterwards, the SD Card will be able to be accessed like a normal part of the filesystem
        """
        if CARD:
            # Create the SD object
            spi = busio.SPI(board.GP18, board.GP19, board.GP16)
            cs = board.GP17
            baud = 8000000
            sd = sdcardio.SDCard(spi, cs, baud)

            # Format the storage
            vfs = storage.VfsFat(sd)

            # Mount the drive and call id /sd
            storage.mount(vfs, '/sd')
        else:
            if not os.path.exists("/sd/"):
                os.mkdir("/sd/")

        # list all files in the drive
        os.listdir('/sd')
        # Default name to save all data to
        self.filename = "local"

    def set_filename(self, filename):
        """ Setter function for the csv filename

        Args:
            filename (str) - formatted name to identify the data from the current session
        Returns:
            None
        """
        self.filename = filename

    def generate_csv(self) -> None:
        """ Sets up the headers on a CSV file

            This is called automatically during initialization for the "local.csv" file
            However, if additional files are desired then this function can be called again with
            a different value for the "filename" parameter

            Args:
                filename (str): [default="local"] Filename to initalize (exclude file suffix)
            Returns:
                None
        """
        # Generate the inital Header row
        headers = "Timestamp,GPS_Latitude,GPS_Longitude,Lightning Distance,Lightning Intensity"

        # Open the file on the sd card to save the lightning data and sent to append "a"
        file = open(f"/sd/{self.filename}.csv", "a")
        file.write(headers+"\n") # need an escape character for csv
        file.close()


    def save(self, packet: str) -> None:
        """ Saves a new packet to an existing CSV file

        If the file has not yet been created, then it should call a function to generate a file
        with the appropriate headers.

        Args:
            packet (str): The compiled string that will be sent over LoRa
        Returns:
            None
        """
        # Generate the full path to the output csv
        filepath = f"/sd/{self.filename}.csv"

        # If the given filename has not been used before, then generate a new one with headers
        if not os.path.exists(filepath):
            self.generate_csv()

        # Open the file on the sd card to save the lightning data and sent to append "a"
        file = open(filepath, "a")
        file.write(packet+"\n") # need an escape character for csv
        file.close()

        # Print Packet for debugging
        print(f"{__name__}\t| DELIVERED={packet}")
