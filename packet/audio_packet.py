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
    pkt_list = []
    if (len(data) > MAX_PACKET_DIGITS_SIZE):
        while (i < len(data)):
            if (len(data)-i <= len(data)%MAX_PACKET_DIGITS_SIZE):
                part= data[i:len(data)]
                i+= len(data)-i
            else:
                part = data[i:i+MAX_PACKET_DIGITS_SIZE]
                i+= MAX_PACKET_DIGITS_SIZE
            pkt_list.append(Packet(PktType.DATA.value,calc_checksum, len(part), msg_counter%MAX_PACKET_DIGITS_SIZE,part))
            msg_counter+=1
    else:
        pkt_list.append(Packet(PktType.DATA.value,calc_checksum, len(data), msg_counter % MAX_PACKET_DIGITS_SIZE, data))
        msg_counter += 1
    return pkt_list

def sendAudioPacket(data, sound_send, sound_recv):
    pkt_list = segmentation(data)
    pkt_list.append(Packet(PktType.FIN.value, calc_checksum, 0, 0,'', PktSide.VICTIM.value))
    sound_recv.start_listening()
    for i in pkt_list:
        sound_send.send(i, sound_recv)
        t0 = time.perf_counter()
        exit = 0
        while(exit == 0):
            rcv_pkt = sound_recv.rcv_pkt()
            if (rcv_pkt != None) and (rcv_pkt.type == PktType.ACK.value) and (i.type== PktType.DATA.value) and (rcv_pkt.seq == i.seq):
                exit = 1
                print('recv ' + str(PktType(rcv_pkt.type)) + ' seq: ' + str(rcv_pkt.seq) + '|' + rcv_pkt.to_string())
            elif (rcv_pkt != None) and (rcv_pkt.type == PktType.FIN.value)and (i.type== rcv_pkt.type) and (rcv_pkt.side == PktSide.ATTACKER.value):
                exit = 1
                print('recv ' + str(PktType(rcv_pkt.type)) + ' from side: ' + str(PktSide(rcv_pkt.side)) + '|' + rcv_pkt.to_string())
            elif (time.perf_counter()-t0 > RECV_TIMEOUT):
                sound_send.send(i, sound_recv)
                t0 = time.perf_counter()
    print('Send audio packet is complete.')
    sound_recv.stop_listening()

def recvAudioPacket(sound_send,sound_recv):
    pkt_list = []
    fin = 0
    sound_recv.start_listening()
    while (fin == 0):
        rcv_pkt = sound_recv.rcv_pkt()
        if (rcv_pkt != None) and (rcv_pkt.type==PktType.DATA.value):
            pkt_list.append(rcv_pkt)
            print('recv ' + str(PktType(rcv_pkt.type)) + ' seq: ' + str(rcv_pkt.seq) + '|' + rcv_pkt.to_string())
            sound_send.send(Packet(PktType.ACK.value, calc_checksum, 0, rcv_pkt.seq), sound_recv)
            sound_recv.cleanBuffers()
        elif (rcv_pkt != None) and (rcv_pkt.type==PktType.FIN.value):
            print('recv ' + str(PktType(rcv_pkt.type)) + ' from side: ' + str(PktSide(rcv_pkt.side)) + '|' + rcv_pkt.to_string())
            sound_send.send(Packet(PktType.FIN.value, calc_checksum, 0, 0,'', PktSide.ATTACKER.value), sound_recv)
            fin = 1
    sound_recv.stop_listening()

    data = ''
    counter = 0
    for i in pkt_list:
        if (i.seq == counter) or ((i.seq > 9) and (i.seq%counter==0)):
            data += i.data
            counter+=1
    print('recv is complete. data is:')
    return data