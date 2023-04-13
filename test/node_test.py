"""
Testing Suite

- Documentation Notes:
    - https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    - https://docs.python.org/3/library/unittest.html
    - https://docs.python.org/3/library/test.html
    - https://realpython.com/python-testing/


"""
import unittest
from test import support

import node


class TestSensorHandling(unittest.TestCase):
    """ Testing the interaction with all sensor modules """

    def test_gps(self):
        """ Test the GPS output
        This will only work if the GPS has the TX/RX, VCC, and GND pins connected
        In addition, the output data will be mostly blank if the antenna is disconnected
        TODO: Test for successful return
        TODO: Test for string format
        TODO: Test for meaningful data
        """
        self.assertEqual(1, 1)

    def test_rtc(self):
        """ Test the RTC output
        [Add any necessary notes about the RTC module]
        [This may use system clock in the early stages]
        TODO: Test for successful return
        TODO: Test for string format
        TODO: Test for meaningful data
        """
        self.assertEqual(1, 1)

    def test_ls(self):
        """ Test the Lightning Sensor output
        [Add any necessary notes about the RTC module]
        [Add any info about simulated vs actual]
        TODO: Test for successful return
        TODO: Test for string format
        TODO: Test for meaningful data
        """
        self.assertEqual(1, 1)


class PacketHandoff(unittest.TestCase):
    """ Testing the handling of any packets, before and after LoRa """

    def test_init_pack(self):
        """ Test the initial GPS Packet that will be sent on startup
        [Add any necessary notes about the RTC module]
        TODO: Test for packet format
        TODO: Test for return name
        TODO: Test for GPIO inactive state on GPS
        """
        name = node.init()
        self.assertEqual(node.NAME, name)

    def test_sens_pack(self):
        """ Test the creation Sensor packet
        Run the entire sensor thread and combine the outputs
        [Add any necessary notes about the RTC module]
        TODO: Test for successful string creation
        TODO: Test for string format
        TODO: Test for pin status
        """
        self.assertEqual(node.collect(), node.NAME + ':,rtc,distance,intensity')

    def test_lora_pack(self):
        """ Test the transmission of the packet over LoRa
        There must be a LoRa module connected
        TODO: Test for SPI/I2C connection with LoRa
        TODO: Test for ability to connect with neighbor
        TODO: Test confirmation response from neighbor
        """
        PACKET_QUEUE = []
        PACKET_QUEUE.append(node.collect())
        self.assertEqual(PACKET_QUEUE[0], PACKET_QUEUE.pop(0))

if __name__ == "__main__":
    unittest.main()
