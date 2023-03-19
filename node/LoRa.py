""" LoRa.py
LoRa Thread Main

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
LoRa Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1_lo_ra.html
"""
from .gpio import lora_rx, lora_tx
from .constants import MPY

if not MPY:
    import logging

# def init() -> str:
#     """ Initializes the Lora connection

#     This will acquire the GPS location and attempt to send it to the server
#     If successful, the server will respond with a string, which will become the reference
#     name for the local node.
#     Afterwards the GPS module should be shut down.

#     Args:
#         None
#     Returns:
#         name (str): the name received from the Server
#     """
#     packet = gps()

#     send(packet)        # Send GPS data to Raspberry Pi
    
#     name = "Node"
#     # while name is None:     # Loop until a name is given
#     #     name = lora_rx()    # Receives new name from the Raspberry Pi FIXME: Add a timeout if it takes too long
#     return name

def send(packet: str) -> None:
    """ Processes Main LoRa communications with packet transfer


    
    Args:
        packet (str): The compiled string that will be sent over LoRa
    Returns:
        None
    
    TODO: Should the return type be none, or should it wait for confirmation?
    """
    # Debug packet
    # if "PACK:" in packet:
    # logging.info("\t%s\t|\tpacket=%s\n", __name__, packet)
    # else:

    # Send Packet
    lora_tx(packet)

    # Confirm delivery FIXME: should this be an affirmation or an accuracy check?
    response = "None"
    # while response is None:     # Loop until a response is found
    #     response = lora_rx()    # Receives a confirmation of reception
    
    if response == "windows":
        logging.info("\t%s\t|\tRunning in Windows Dev Mode: %s", __name__, packet)
    elif response == "disabled":
        logging.info("\t%s\t|\tLoRa Module Disabled: %s", __name__, packet)
    else:
        if MPY:
            print(f"{__name__}\t|\tDELIVERED={packet}")
        else:
            logging.info("\t%s\t|\tDELIVERED=%s\n", __name__, packet)

    # else:
        # logging.error("\t%s\t|\tResponse was different...", __name__)
