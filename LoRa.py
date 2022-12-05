"""
LoRa Thread Main
"""
import time
import threading


class LoRa(threading.Thread):
    """
    LoRa thread class
    """
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def shutdown(self, signum, frame):
        """
        Closes the th
        """
        print("Shutting down LoRa thread...")

    def run(self) -> None:
        """
        This thread will process all LoRa communications
        TODO: Implement RX
        TODO: Implement TX
        TODO: Add ability to kill thread
        TODO: Add ability to detect new packets to send
        TODO: Add LoRa setup process
        """

        while True:
            if global stopflag:
                break
            print("LoRa")
            time.sleep(1)

    def get_id(self):
        """
        Gets the ID of the current thread
        """
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        """
        Raises an exception to kill the thread
        """
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')