""" sensor.py
Sensor Thread
This file in the module will handle the packaging of sensor data
It will be responsible for the GPIO interface with sensor equipment

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
LoRa Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1sensor.html
"""
from .gpio import Devices

class Reader:
    """ Reads the sensors """
    def __init__(self, devices, name="") -> None:
        self.name = name
        self.devices = devices

    def setname(self, name: str) -> None:
        """ Modifies name identifier of current node

        The purpose for having the name is to reduce power consumption from the GPS.
        By only acquiring the GPS data on startup, the GPS can be turned off after first measurement.
        The node still must distinguish itself from other nodes, so the server will assign a name.

        Args:
            name (str): name assigned to node by server
        Returns:
            None
        """
        self.name = name
        print(f"{__name__}\t|\tThis Node is now named:\t{self.name}")


    def collect(self) -> str:
        """ Collects data from sensors and compiles it into a string

        This thread will handle all communications with the sensors and create new packets

        Args:
            None
        Returns:
            packet (str): The properly formatted packet to be passed to LoRa
        """
        # When lightning is detected, this will populate the string with the sensor data
        lng: str = self.devices.lightning()       # Acquire Lightning Distance/Intensity

        # Acquire RTC Timestamp
        tstmp: str = self.devices.timestamp()

        # Acquire GPS Packet
        gps: str = self.devices.gps_lat_long

        # Append to PACKET_QUEUE
        packet: str = f"STK:{self.name},{tstmp},{lng},{gps}"
        print(f"{__name__}\t|\tCREATED={packet}")

        return packet
