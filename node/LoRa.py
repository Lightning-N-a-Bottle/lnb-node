""" LoRa.py
LoRa Thread Main

Git Repo: https://github.com/Lightning-N-a-Bottle/lnb-node
Main Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/index.html
LoRa Doxygen: https://lightning-n-a-bottle.github.io/lnb-node/docs/html/namespacenode_1_1_lo_ra.html
"""
# from .gpio import lora_tx
# from .constants import MPY

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
    # lora_tx(packet)

    print(f"{__name__}\t|\tDELIVERED={packet}")

    # else:
        # logging.error("\t%s\t|\tResponse was different...", __name__)
