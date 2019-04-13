from packet.packet_constants import *
from packet.err_detection import *
from sound.sound_encoder import *
from sound.sound_decoder import *
import sound.sound_decoder
from packet.packet import *
import time
#from datetime import datetime

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
        if (i.type == DATA_PACKET)or ((i.type== FIN_PACKET)):
            print('send packet: '+str(i.seq))
            soundRecv.stop_listening()
            soundSend.send(i.toString())
            #soundRecv.start_listening()
        # elif (i.type== FIN_PACKET):
        #     print('send fin packet')
        #     soundRecv.stop_listening()
        #     soundSend.send(i.finPacket2Str())
        #     soundRecv.start_listening()
        soundRecv.start_listening()
        t0= time.perf_counter()
        while((soundRecv.recvPkt()==None)
              or(soundRecv.recvPkt().type==DATA_PACKET)
              or(soundRecv.recvPkt().seq != i.seq)
              or(soundRecv.recvPkt().checksum != calcCheckSum(soundRecv.recvPkt()))):
            if (time.perf_counter()-t0 > RECV_TIMEOUT):
                soundRecv.stop_listening()
                soundSend.send(i.toString())
                soundRecv.start_listening()
                t0= time.perf_counter()
            if (soundRecv.recvPkt()!=None and soundRecv.recvPkt().type==DATA_PACKET):
                soundRecv.stop_listening()
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
            pktList.insert(seqNum, soundRecv.recvPkt())
            soundRecv.stop_listening()
            print('send ack for packet: ' + str(seqNum))
            soundSend.send(Packet(ACK_PACKET, calcCheckSum, 0, seqNum).toString())
            soundRecv.start_listening()
    soundRecv.stop_listening()

    if (soundRecv.recvPkt().type==FIN_PACKET):
        print('get Fin packet')
        soundSend.send(Packet(FIN_PACKET, calcCheckSum).toString())
        print('send fin packet')

    data = ''
    for i in pktList:
        data += i.data
    print('recv is complete. data is: ', data)
    return data