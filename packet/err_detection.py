from packet.packet_constants import *
from packet.packet import *

def calc_checksum(pkt):
    checksum = (bsd_checksum(pkt))
    return ((checksum)%MAX_BYTE_SIZE)

def bsd_checksum(pkt):
    data = pkt.to_byte_array()
    checksum = 0
    for b in data:
        checksum = (checksum&0xff >> 1) + ((checksum&1) << 7)
        checksum = checksum + b
        checksum = checksum&0xff
    return checksum