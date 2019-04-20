from packet.packet_constants import *
from packet.err_detection import *
from sound.sound_encoder import *
from sound.sound_decoder import *
import sound.sound_decoder
from packet.packet import *
import time

def segmentation(data):
    i = 0
    msg_counter = 0
    packetsList = []
    if (len(data)>MAX_PACKET_DIGITS_SIZE):
        while (i<len(data)):
            if (len(data)-i<= len(data)%MAX_PACKET_DIGITS_SIZE):
                part= data[i:len(data)]
                i+= len(data)-i
            else:
                part = data[i:i+MAX_PACKET_DIGITS_SIZE]
                i+= MAX_PACKET_DIGITS_SIZE
            packetsList.append(Packet(PktType.DATA.value,calcCheckSum, len(part), msg_counter%MAX_PACKET_DIGITS_SIZE,part))
            msg_counter+=1
    else:
        packetsList.append(Packet(PktType.DATA.value,calcCheckSum, len(data), msg_counter % MAX_PACKET_DIGITS_SIZE, data))
        msg_counter += 1
    return packetsList

def sendAudioPacket(data, soundSend,soundRecv):
    pktList= segmentation(data)
    pktList.append(Packet(PktType.FIN.value, calcCheckSum, PktSide.VICTIM.value))

    for i in pktList:
        soundSend.send(i, soundRecv)
        t0= time.perf_counter()
        while((soundRecv.recvPkt()==None)
              or(soundRecv.recvPkt().type==PktType.DATA.value)
              or(soundRecv.recvPkt().seq != i.seq)):
            if (time.perf_counter()-t0 > RECV_TIMEOUT):
                soundSend.send(i, soundRecv)
                t0= time.perf_counter()
            if (soundRecv.recvPkt()!=None and soundRecv.recvPkt().type==PktType.DATA.value):
                soundRecv.start_listening() #Clean recv buffers
        soundRecv.stop_listening()
        if (soundRecv.recvPkt().type==PktType.ACK.value):
            print('recv ack for packet: ' + str(i.seq))
        elif(soundRecv.recvPkt().type==PktType.FIN.value) and (soundRecv.recvPkt().side == PktSide.ATTACKER.value):
            print('recived FIN_ACK')
    print('send packets is complete.')

def recvAudioPacket(soundSend,soundRecv):
    pktList = []
    t0 = time.perf_counter()
    soundRecv.start_listening()
    while ((soundRecv.recvPkt() == None)
           or (soundRecv.recvPkt().type != PktType.FIN.value)):
        if ((soundRecv.recvPkt() != None) and (soundRecv.recvPkt().type == PktType.DATA.value)):
            pkt = soundRecv.recvPkt()
            seqNum = pkt.seq
            pktList.append(soundRecv.recvPkt())
            soundSend.send(Packet(PktType.ACK.value, calcCheckSum, 0, seqNum), soundRecv)
            t0 = time.perf_counter()
        # elif (time.perf_counter()-t0 > RECV_TIMEOUT-3):
        #         soundRecv.start_listening() #clean th buffer
        #         t0= time.perf_counter()
    soundRecv.stop_listening()

    if ((soundRecv.recvPkt().type==PktType.FIN.value) and (soundRecv.recvPkt().side == PktSide.VICTIM.value)):
        soundSend.send(Packet(PktType.FIN.value, calcCheckSum, PktSide.ATTACKER.value), soundRecv)

    data = ''
    counter = 0
    for i in pktList:
        if (i.seq== counter):
            data += i.data
            counter+=1
    print('recv is complete. data is:')
    return data