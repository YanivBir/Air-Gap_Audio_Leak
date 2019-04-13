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

            packetsList.append(Packet(DATA_PACKET,calcCheckSum, len(part), msg_counter%MAX_PACKET_DIGITS_SIZE,part))
            msg_counter+=1
    else:
        packetsList.append(Packet(DATA_PACKET,calcCheckSum, len(data), msg_counter % MAX_PACKET_DIGITS_SIZE, data))
        msg_counter += 1
    return packetsList

def sendAudioPacket(data, soundSend,soundRecv):
    pktList= segmentation(data)
    pktList.append(Packet(FIN_PACKET, calcCheckSum))

    for i in pktList:
        soundSend.send(i, soundRecv)
        t0= time.perf_counter()
        while((soundRecv.recvPkt()==None)
              or(soundRecv.recvPkt().type==DATA_PACKET)
              or(soundRecv.recvPkt().seq != i.seq)
              or(soundRecv.recvPkt().checksum != calcCheckSum(soundRecv.recvPkt()))):
            if (time.perf_counter()-t0 > RECV_TIMEOUT):
                soundSend.send(i, soundRecv)
                t0= time.perf_counter()
            if (soundRecv.recvPkt()!=None and soundRecv.recvPkt().type==DATA_PACKET):
                soundRecv.start_listening() #Clean recv buffers
        soundRecv.stop_listening()
        if (soundRecv.recvPkt().type==ACK_PACKET):
            print('recv ack for packet: ' + str(i.seq))
        elif(soundRecv.recvPkt().type==FIN_PACKET):
            print('recived FIN_ACK')
    print('send packets is complete.')

def recvAudioPacket(soundSend,soundRecv):
    pktList = []
    soundRecv.start_listening()
    while ((soundRecv.recvPkt() == None)
           or (soundRecv.recvPkt().type != FIN_PACKET)
           or (soundRecv.recvPkt().checksum != calcCheckSum(soundRecv.recvPkt()))):
        if (soundRecv.recvPkt() != None and soundRecv.recvPkt().type == DATA_PACKET):
            seqNum = soundRecv.recvPkt().seq
            print('get packet: ' + str(seqNum))
            pktList.append(soundRecv.recvPkt())
            soundSend.send(Packet(ACK_PACKET, calcCheckSum, 0, seqNum), soundRecv)
    soundRecv.stop_listening()

    if (soundRecv.recvPkt().type==FIN_PACKET):
        soundSend.send(Packet(FIN_PACKET, calcCheckSum), soundRecv)

    data = ''
    counter = 0
    for i in pktList:
        if (i.seq== counter):
            data += i.data
            counter+=1
    print('recv is complete. data is:')
    return data