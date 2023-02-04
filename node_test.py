"""
Testing Suite

- Documentation Notes:
    - https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    - https://docs.python.org/3/library/unittest.html
    - https://docs.python.org/3/library/test.html
    - https://realpython.com/python-testing/


"""
import logging
import unittest
from test import support
import sys

import node

class TestSensorHandling(unittest.TestCase):
    """
    Class of Node Test Cases
    """

    def test_gps(self):
        """Test the GPS output
        This will only work if the GPS has the TX/RX, VCC, and GND pins connected
        In addition, the output data will be mostly blank if the antenna is disconnected
        
        """
        self.assertEqual(1, 1)

    def test_rts(self):
        self.assertEqual(1, 1)

    def test_ls(self):
        self.assertEqual(1, 1)

    def test_sensors(self):
        self.assertEqual(1, 1)

class PacketHandoff(unittest.TestCase):

    def test_pq1(self):
        self.assertEqual(node.collect(), '-1')
    def test_pq2(self):
        PACKET_QUEUE = []
        PACKET_QUEUE.append(node.collect())
        self.assertEqual(PACKET_QUEUE[0], PACKET_QUEUE.pop(0))

if __name__ == "__main__":
    sys.exit(unittest.main())