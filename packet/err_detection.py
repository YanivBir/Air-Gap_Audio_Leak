from packet.packet_constants import *
from packet.packet import *

def bsd_checksum(pkt):
    data = pkt.to_byte_array()
    checksum = 0
    for b in data:
        checksum = (checksum&0xff >> 1) + ((checksum&1) << 7)
        checksum = checksum + b
        checksum = checksum&0xff
    return checksum

def calc_checksum(pkt):
    checksum_str = str(bsd_checksum(pkt))
    right = 0
    if (checksum_str[2:]!=''):
        right = int (checksum_str[2:])
    left = 0
    if (checksum_str[:2]!=''):
        left = int(checksum_str[:2])
    return (right+left)