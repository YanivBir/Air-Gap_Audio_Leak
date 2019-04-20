from packet.packet_constants import *
from packet.err_detection import *

class Packet:
    def __init__(self, type,checksumFunc=None, len=0, seq=0, data='', side=0):
        self._type =type
        self._len = len
        self._seq = seq
        self._data = data
        self._side = side
        if (checksumFunc!=None):
            self._checksum = checksumFunc(self)

    def get_type(self):
        return self._type
    def set_type(self, typed):
        self._type = typed
    type = property(get_type, set_type)

    def get_len(self):
        return self._len
    def set_len(self, len):
        self._len = len
    len = property(get_len, set_len)

    def get_seq(self):
        return self._seq
    def set_seq(self, seq):
        self._seq = seq
    seq = property(get_seq, set_seq)

    def get_checksum(self):
        return self._checksum
    def set_checksum(self, checksum):
        self._checksum = checksum
    checksum =property(get_checksum, set_checksum)

    def get_data(self):
        return self._data
    def set_data(self, data):
        self._data = data
    data = property(get_data, set_data)

    def get_side(self):
        return self._side
    def set_side(self, side):
        self._side = side
    side = property(get_side, set_side)

    def toString(self):
        strPkt = 'r' + str(self.type)
        if (self.type == PktType.DATA.value):
            strPkt+= str(self.len).zfill(SIZE_OF_BYTE)+str(self.seq)+str(self.checksum).zfill(SIZE_OF_BYTE)+self.data
        elif (self.type == PktType.ACK.value):
            strPkt+=  str(self.seq)+ str(self.checksum).zfill(SIZE_OF_BYTE)
        elif (self.type== PktType.FIN.value):
            strPkt+= str(self.checksum).zfill(SIZE_OF_BYTE)+ str(self.side)
        strPkt+= '0'
        return strPkt