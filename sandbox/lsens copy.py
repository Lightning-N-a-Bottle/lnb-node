import as3935
import RPi.GPIO as GPIO
import time
import signal

irq_pin_number = 11    # BCM number (code after GPIO)
bus = 1               # On newer Raspberrys is 1
address = 0x03        # If using MOD-1016 this is the address

BRK = False

sensor = as3935.AS3935(irq_pin_number, bus, address)

# We need to calibrate the sensor first. Use the tuning cap provided
# or calculate it using sensor.calculate_tuning_cap(*args)
# print(sensor.calculate_tuning_cap())
sensor.full_calibration(12)

sensor.set_indoors(True)


def handler(signum, frame) -> None:
    print("Cleaning up GPIO pins")
    GPIO.cleanup()
    global BRK
    BRK = True

# Every time you sense a pulse on IRQ it means there is an
# interruption request. You can read it like this:
def irq_callback(gpio):
    interruption = sensor.get_interrupt()
    if interruption == as3935.INT_NH:
        print("Noise floor too high")
    elif interruption == as3935.INT_D:
        print("Disturbance detected. Mask it?")
    elif interruption == as3935.INT_L:
        print("Lightning detected!")
        distance = sensor.get_distance()
        print(distance)

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(irq_pin_number, GPIO.IN)
    GPIO.add_event_detect(irq_pin_number, GPIO.RISING, callback=irq_callback)
    # cb = sensor.pi.callback(irq_pin_number, pigpio.RISING_EDGE, irq_callback)
    print("Ready...")
    while not BRK:
        distance = sensor.get_distance()
        print(distance)
        time.sleep(1)
        pass
finally:
    print("Finished!")
    # cb.cancel()
    sensor.pi.stop()