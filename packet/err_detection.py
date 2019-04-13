from packet.packet_constants import *
from packet.packet import *

def calcCheckSum(pkt):
    checksum = int(pkt.type)
    if (pkt.type == DATA_PACKET):
        checksum+= int(pkt.len)
        checksum+= int(pkt.seq)
        i = 0
        while (i< len(pkt.data)):
            if (i+SIZE_OF_BYTE < len(pkt.data)):
                byte = pkt.data[i:i+SIZE_OF_BYTE]
            else:
                byte = pkt.data[i:i+len(pkt.data)]
            checksum+= int(byte)
            i=i+SIZE_OF_BYTE
    elif(pkt.type == ACK_PACKET):
        checksum+= int(pkt.seq)

    checksum = int(checksum%(MAX_BYTE_SIZE))
    return checksum