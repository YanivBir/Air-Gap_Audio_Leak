from packet.packet_constants import *
from packet.err_detection import *
from sound.sound_encoder import *
from sound.sound_decoder import *
import sound.sound_decoder
from packet.packet import *
import time
#from datetime import datetime

# def buildDataPacket(data, seq):
#     dataPkt = Packet()
#     dataPkt.seq = seq
#     dataPkt.len = len(data)
#     dataPkt.data = data
#     dataPkt.type = DATA_PACKET
#     dataPkt.checksum = calcCheckSum(dataPkt)
#     return dataPkt

def buildAckPacket(seq):
    ackPacket = Packet()
    ackPacket.seq = seq
    ackPacket.type = ACK_PACKET
    ackPacket.checksum = calcCheckSum(ackPacket)
    return ackPacket

def buildFinPacket():
    finPacket = Packet()
    finPacket.type = FIN_PACKET
    finPacket.checksum = calcCheckSum(finPacket)
    return finPacket

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

            packetsList.append(Packet(DATA_PACKET, len(part), msg_counter%MAX_PACKET_DIGITS_SIZE, part))
            msg_counter+=1
    else:
        packetsList.append(Packet(DATA_PACKET, len(data), msg_counter % MAX_PACKET_DIGITS_SIZE, data))
        msg_counter += 1
    return packetsList

def sendAudioPacket(data, soundSend,soundRecv):
    pktList= segmentation(data)
    pktList.append(buildFinPacket())
    for i in pktList:
        if (i.type == DATA_PACKET):
            print('send packet: '+str(i.seq))
            soundRecv.stop_listening()
            soundSend.send(i.dataPacket2Str())
            soundRecv.start_listening()
        elif (i.type== FIN_PACKET):
            print('send fin packet')
            soundRecv.stop_listening()
            soundSend.send(i.finPacket2Str())
            soundRecv.start_listening()
        soundRecv.start_listening()
        t0= time.perf_counter()
        while((soundRecv.recvPkt()==None)
              or(soundRecv.recvPkt().type==DATA_PACKET)
              or(soundRecv.recvPkt().seq != i.seq)
              or(soundRecv.recvPkt().checksum != calcCheckSum(soundRecv.recvPkt()))):
            if (time.perf_counter()-t0 > RECV_TIMEOUT):
                soundRecv.stop_listening()
                soundSend.send(i.dataPacket2Str()) #add also section to FIN_PACKET
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
    #pkt = Packet()
    # while (pkt.type != FIN_PACKET):
    #     pkt = soundRecv.recive()
    #     while (pkt.checksum != calcCheckSum(pkt)):
    #         pkt = soundRecv.recive()
    #     print('recv packet type:' + str(pkt.type))
    #     if (pkt.type == DATA_PACKET):
    #         pktList.insert(pkt.seq, pkt)
    #         soundSend.send(buildAckPacket(pkt.seq).ackPacket2Str())
    #         print('send ack packet ' + str(pkt.seq))
    # if (pkt.type == FIN_PACKET):
    #     soundSend.send(pkt.finPacket2Str())
    #     print('send ack to recived FIN')
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
            soundSend.send(buildAckPacket(seqNum).ackPacket2Str())
            soundRecv.start_listening()
    soundRecv.stop_listening()

    if (soundRecv.recvPkt().type==FIN_PACKET):
        print('get Fin packet')
        soundSend.send(buildFinPacket().finPacket2Str())
        print('send fin packet')

    data = ''
    for i in pktList:
        data += i.data
    print('recv is complete. data is: ', data)
    return data