# Test Code
# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Example for Pico. Turns the built-in LED on and off with no delay."""
import board
import digitalio
import time
import busio

#Create a digitalIO  object for the board LED (Its Green)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#Create an digital IO object labeled LEDGreen which is connected to GPIO 14 (Pin19) and a green LED
ledGreen = digitalio.DigitalInOut(board.GP14)
ledGreen.direction = digitalio.Direction.OUTPUT

# Create a digitalIO object labeled button which is connected to GPIO 13 and to a Button
button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.DOWN)

while True:
    if(button.value != 0):
        ledGreen.value = True
    else:
        ledGreen.value = False

