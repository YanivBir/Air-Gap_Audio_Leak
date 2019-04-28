from packet.packet_constants import *
from packet.packet import *

def calc_checksum(pkt):
    return bsd_checksum(pkt)%MAX_BYTE_SIZE
    # checksum = int(pkt.type)
    # if (pkt.type == PktType.DATA.value):
    #     checksum+= int(pkt.len)
    #     checksum+= int(pkt.seq)
    #     i = 0
    #     while (i< len(pkt.data)):
    #         if (i+SIZE_OF_BYTE < len(pkt.data)):
    #             byte = pkt.data[i:i+SIZE_OF_BYTE]
    #         else:
    #             byte = pkt.data[i:i+len(pkt.data)]
    #         checksum+= int(byte)
    #         i=i+SIZE_OF_BYTE
    # elif(pkt.type == PktType.ACK.value):
    #     checksum+= int(pkt.seq)
    # elif(pkt.type == PktType.FIN.value):
    #     checksum+= int (pkt.side)
    # else:
    #     print('checksum() error type')
    #     return -1

    # checksum = int(checksum%(MAX_BYTE_SIZE))
    # return checksum

def bsd_checksum(pkt):
    data = pkt.to_byte_array()
    checksum = 0
    for b in data:
        checksum = (checksum&0xff >> 1) + ((checksum & 1) << 7)
        checksum = checksum + b
        checksum = checksum &0xff
    return checksum