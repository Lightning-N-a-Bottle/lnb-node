# LNB Sensor Node

The code that will go into the sensor nodes to record and transmit data

## Setup Process

The process for setting up the code and flashing it to the device is listed below. Eventually I plan on scripting this process with a bash file so that it is automated.

1. Clone Git Repo on local device
2. Switch to desired branch
3. Run `pip install -r requirements.txt`
4. Move the code to the RPi Pico if not there already

## Functions

1. Record data from storms
   1. Internal RTC Time of strike
   2. GPS Location of node
   3. Distance of Strike from Node
   4. Energy value recorded from AS3935 (Not necessarily useful, but included)
   5. Whether it is a disturber or a strike

## Software Flowchart

### Initial Setup

1. Initialize GPS Module
    1. Wait until a fix is acquired
    2. Use NMEA data to initialize the internal RTC (GPS delivers up to 1 second accuracy)
    3. Use NMEA data to record the current GPS latitude and longitude
    4. Turn off the GPS
2. Initialize the AS3935 lightning sensor
3. Initialize the Storage class object
4. Run the Sensor.collect() function and append return to PACKET_QUEUE (or launch as a thread if multithreading)
5. Run the Storage.save function with the PACKET_QUEUE as an input

### Sensor Class (Thread 1 if needed)

1. A lightning strike is detected
2. Read in the sensor data for distance
3. Read in the exact RTC module time
5. Package this all up in a comma separated string that includes the GPS measured initially
6. Set a flag that will be read by Thread 2 to indicate that there is at least one packet to be sent.

### Storage Class (Thread 2 if needed)

1. This thread will be responsibly for Micro SD control. It will automatically interface with the micro SD module whenever a new packet is detected from the first thread (see step 6 above).
2. This will handle the GPIO connection to the sd module as well as the csv formatting and file structure.
4. Send the packet across through whatever structure we decided on previously.
5. We could add a handshake to confirm that the packet was sent properly, however this may be too complex, unnecessary, or slow.

### Documentation

The source code comments aim to follow PEP8 and Doxygen requirements, and an html webpage has been generated using doxygen* for documentation purposes.
To recompile the Doxygen html generation, simply run `"doxygen lnb-node"` from the project directory

*NOTE: the files generated from doxygen are too large to be transferred onto the pico storage. We will have a separage branch that excludes the doxygen files so that the program can be directly cloned onto the pico
