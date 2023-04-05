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

class Storage:
    """ Class set  """
    def __init__(self):
        """ Initial setup for the SD Card
        
            This will create an SD Card object, format it, then mount it to the filesystem
            Afterwards, the SD Card will be able to be accessed like a normal part of the filesystem
        """
        # Create the SD object
        spi = busio.SPI(board.GP18, board.GP19, board.GP16)
        cs = board.GP17
        baud = 8000000
        sd = sdcardio.SDCard(spi, cs, baud)

        # Format the storage
        vfs = storage.VfsFat(sd)

        # Mount the drive and call id /sd
        storage.mount(vfs, '/sd')

        # list all files in the drive
        os.listdir('/sd')

        # Generate initial CSV
        self.generate_csv()


    def generate_csv(self, filename="local") -> None:
        """ Sets up the headers on a CSV file

            This is called automatically during initialization for the "local.csv" file
            However, if additional files are desired then this function can be called again with
            a different value for the "filename" parameter

            Args:
                filename (str): [default="local"] Filename to initalize (exclude file suffix)
            Returns:
                None
            TODO: Add a safety to prevent calling this on an already existing file (see TODO in self.save())
        """
        headers = "Timestamp,GPS_Latitude,GPS_Longitude,Lightning Distance,Lightning Intensity"

        # Open the file on the sd card to save the lightning data and sent to append "a"
        file = open(f"/sd/{filename}.csv", "a")
        file.write(headers+"\n") # need an escape character for csv
        file.close()


    def save(self, packet: str, filename="local") -> None:
        """ Saves a new packet to an existing CSV file

        Args:
            packet (str): The compiled string that will be sent over LoRa
            filename (str): [default="local"] Filename to append the packet (exclude file suffix)
        Returns:
            None
        TODO: Add a safety to prevent calling this on an uninitialized file, maybe call generate_csv() here if new file
        """

        # Open the file on the sd card to save the lightning data and sent to append "a"
        file = open(f"/sd/{filename}.csv", "a")
        file.write(packet+"\n") # need an escape character for csv
        file.close()

        # Print Packet for debugging
        print(f"{__name__}\t|\tDELIVERED={packet}")
