# LNB Sensor Node

The code that will go into the sensor nodes to record and transmit data

## Setup Process

The process for setting up the code and flashing it to the device is listed below. Eventually I plan on scripting this process with a bash file so that it is automated.

1. Clone Git Repo on local device
2. Download and install conda, if not already done
    1. Windows: https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Windows-x86_64.exe
    2. Linux/Raspbian: https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-aarch64.sh
        1. Navigate to the conda directory (`"C:\Users\{Current_User}\miniconda3\Scripts"` on Windows)
        2. Run `./conda init --verbose`
        3. Restart all terminals (if vscode, restart the whole IDE)
3. Create a conda environment from the yml file
4. Flash the desired branch to the RPi (Pico/Zero) module

## Functions

1. Record data from storms
   1. RTC Time
   2. GPS Location
   3. Strike Distance
   4. Intensity?
2. Transmit data packets to Server through LoRa
3. [Optional] Receive packets from other Nodes (mesh)

## Software Flowchart

1. **_[TODO: This part is potentially run in multiple threads]_**
2. **_[FIXME: If we are doing mesh, then we will need to account for both TX and RX_**

### Thread 1

1. A lightning strike is detected
2. Read in the sensor data for distance
3. Read in the exact RTC module time
4. Read in the GPS Location **_[FIXME: should this be measured every time or should we store the location on the server during initial setup/handshake and assume it doesn't move?]_**
5. Package this all up in some form of struct **_[TODO: Decide on best format. What can LoRa transmit best? JSON, CSV, dict, string, etc.]_**
6. **_[FIXME: How do we indicate to the second thread that there is a packet ready to be sent? Ideas listed below]_**
    1. Set a flag that will be read by Thread 2 to indicate that there is at least one packet to be sent. The second thread can then be set on a schedule to send/clear out all packets every hour or so.
    2. If each package has it's own output file, the second thread could check the output directory for new files, send them immediately, and then delete them afterwards. Does the RPi Pico have a file structure?

### Thread 2

1. This thread will be responsibly for LoRa control. It will either run on a schedule, or it will run whenever a new packet is detected from the first thread (see step 6 above).
2. If we decide to use mesh, then this will also handle receiving from other Nodes that can't reach the Server on their own.
3. Once this thread decides to send a packet, it should establish a connection with the server to ensure that it is listening
    1. **_[TODO: Figure out how to do this, whether it is through pinging or through pyLoRa features]_**
4. Send the packet across through whatever structure we decided on previously.
5. We could add a handshake to confirm that the packet was sent properly, however this may be too complex, unnecessary, or slow.
