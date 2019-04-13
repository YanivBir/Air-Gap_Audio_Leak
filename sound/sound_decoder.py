from __future__ import division  # float division of integers
from collections import deque
import pyaudio
import struct
import math
import numpy
import sys
import threading
from sound.sound_constants import *
from packet.audio_packet import *
import huffman.huffman as huffman
import huffman.freq as freq
from packet.packet import *

class Decoder:
    def __init__(self):
        self.win_len = 2*int(BIT_DURATION*RATE / CHUNK_SIZE / 2)
        self.win_fudge = int(self.win_len / 2)
        self.buf_len = self.win_len + self.win_fudge
        self.audio_buffer = deque()
        self.bits_buffer = []
        self.idlecount = 0
        self.character_callback = None
        self.idle_callback = None
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=AUDIOBUF_SIZE)
        self.do_listen = False
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def listen(self):
        self.packet= None
        self.bits_buffer = []
        while (True):
            while (self.do_listen):
                audiostr = self.stream.read(CHUNK_SIZE)
                self.audio = list(struct.unpack("%dh" % CHUNK_SIZE, audiostr))
                self.window()
                power = []
                power.append(self.goertzel(ZERO_FRQ))
                power.append(self.goertzel(ONE_FRQ))
                power.append(self.goertzel(TWO_FRQ))
                power.append(self.goertzel(THREE_FRQ))
                power.append(self.goertzel(FOUR_FRQ))
                power.append(self.goertzel(FIVE_FRQ))
                power.append(self.goertzel(SIX_FRQ))
                power.append(self.goertzel(SEVEN_FRQ))
                power.append(self.goertzel(EIGHT_FRQ))
                power.append(self.goertzel(NINE_FRQ))
                power.append(self.goertzel(RESET_FRQ))
                base = self.goertzel(BASE_FRQ)
                self.update_state(power, base)
                self.signal_to_bits()
                bits_string = ''.join(self.bits_buffer)

                if (len(bits_string)>1):
                    pointer = 1 #because 'r' is the first 'bit'
                    type = int (bits_string[pointer:pointer+TYPE_SIZE]) #The type field
                    pointer+= TYPE_SIZE
                    if(type==ACK_PACKET):
                        if(len(bits_string)== ACK_PACKET_SIZE):
                            self.packet = Packet(ACK_PACKET,None,0, int(bits_string[pointer:pointer+SEQ_SIZE]))
                            pointer += SEQ_SIZE
                            self.packet.checksum = int(bits_string[pointer:pointer+CHECKSUM_SIZE])
                    elif(type==FIN_PACKET):
                        if(len(bits_string)==FIN_PACKET_SIZE):
                            self.packet = Packet(FIN_PACKET)
                            self.packet.checksum = int(bits_string[pointer:pointer + CHECKSUM_SIZE])
                    elif(type==DATA_PACKET):
                        if(len(bits_string)> DATA_PACKET_SIZE):
                            length= int(bits_string[pointer:pointer+LEN_SIZE]) #The length field
                            pointer+= LEN_SIZE
                            if(length+ DATA_PACKET_SIZE==len(bits_string)):
                                seq = int(bits_string[pointer:pointer + SEQ_SIZE])
                                pointer+= SEQ_SIZE
                                checksum = int(bits_string[pointer:pointer + CHECKSUM_SIZE])
                                pointer+= CHECKSUM_SIZE
                                data = bits_string[pointer:pointer + length]
                                self.packet = Packet(DATA_PACKET, None, length, seq, data)
                                self.packet.checksum = checksum
                    else:
                        self.bits_buffer=[]
            #self.closeChannel()
        #return -1
                #if (length + DATA_PACKET_SIZE == len(bits_string)):
                #     data = getData(bits_string)
                #     if (data==-1):
                #         self.do_listen = False
                #         break
                #     if (data == CLOSE_PACKET_MARK):
                #         self.do_listen = False
                #     else:
                #         self.all_data += str(data)
                #     self.bits_buffer = []

        # if (self.all_data!=''):
        #     freq_dict = freq.relative_english_freq()
        #     freqs = list(freq_dict.items())  # HuffmanCode requires (symbol, freq) pairs.
        #
        #     decimal_huffman = huffman.HuffmanCode(freqs, 10)
        #     enc_data = decimal_huffman.decode(self.all_data) #move it from here

            # move the next section from here
            #print(enc_data)
            #fd = open(STOLEN_FILE, 'w')
            #fd.write(enc_data)
            #fd.close()

        #self.stream.stop_stream()
        #self.stream.close()
        #self.p.terminate()

    def closeChannel (self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def attach_character_callback(self, func):
        self.character_callback = func

    def attach_idle_callback(self, func):
        self.idle_callback = func

    def start_listening(self):
        self.bits_buffer = []
        self.packet = None
        self.do_listen = True

    def stop_listening(self):
        self.do_listen = False

    def recvPkt(self):
        return self.packet

    def cleanRecvPkt(self):
        self.packet = None

    # Takes the raw noisy samples of -1/0/1 and finds the bitstream from it
    def signal_to_bits(self):
        if len(self.audio_buffer) < self.buf_len:
            return
        buf = list(self.audio_buffer)
        costs = [[] for i in range(STATES)]
        for i in range(self.win_fudge):
            win = buf[i: self.win_len + i]
            costs[ZERO_STATE].append(sum(x!=ZERO_STATE for x in win))
            costs[ONE_STATE].append(sum(x!=ONE_STATE for x in win))
            costs[TWO_STATE].append(sum(x!=TWO_STATE for x in win))
            costs[THREE_STATE].append(sum(x != THREE_STATE for x in win))
            costs[FOUR_STATE].append(sum(x != FOUR_STATE for x in win))
            costs[FIVE_STATE].append(sum(x != FIVE_STATE for x in win))
            costs[SIX_STATE].append(sum(x != SIX_STATE for x in win))
            costs[SEVEN_STATE].append(sum(x != SEVEN_STATE for x in win))
            costs[EIGHT_STATE].append(sum(x != EIGHT_STATE for x in win))
            costs[NINE_STATE].append(sum(x != NINE_STATE for x in win))
            costs[REST_STATE].append(sum(x!=REST_STATE for x in win))
            costs[UNDEFINED_STATE].append(sum(x!=-1 for x in win))
        min_costs = [min(costs[i]) for i in range(STATES)]
        min_cost = min(min_costs)
        signal = min_costs.index(min_cost)
        fudge = costs[signal].index(min_cost)
        for i in range(self.win_len + fudge):
            self.audio_buffer.popleft()
        # If we got a signal, put it in the byte!
        if signal < REST_STATE:
            self.bits_buffer.append(str(signal))
        # If we get a charstart signal, reset byte!
        elif signal == REST_STATE:
            #for bit in self.bits_buffer:
            #    print(bit, end='', flush=True)
            self.bits_buffer = []
            self.bits_buffer.append('r')
        # If we get no signal, increment idlecount if we are idling
        if signal == UNDEFINED_STATE:
            self.idlecount += 1
        else:
            self.idlecount = 0
        if self.idlecount > IDLE_LIMIT and self.idle_callback:
            self.idlecount = 0
            self.idle_callback()

    # Determine the raw input signal of silences, 0s, and 1s. Insert into sliding window.
    def update_state(self, power, base):
        state = -1
        #chking from the high frq to the low
        if power[NINE_STATE] / base > NINE_THRESH:
             state = NINE_STATE
        elif power[EIGHT_STATE] / base > EIGHT_THRESH:
             state = EIGHT_STATE
        elif power[SEVEN_STATE] / base > SEVEN_THRESH:
             state = SEVEN_STATE
        elif power[SIX_STATE] / base > SIX_THRESH:
            state = SIX_STATE
        elif power[FIVE_STATE] / base > FIVE_THRESH:
             state = FIVE_STATE
        elif power[FOUR_STATE] / base > FOUR_THRESH:
            state = FOUR_STATE
        elif power[THREE_STATE] / base > THREE_THRESH:
            state = THREE_STATE
        elif power[TWO_STATE] / base > TWO_THRESH:
            state = TWO_STATE
        elif power[ONE_STATE] / base > ONE_THRESH:
            state = ONE_STATE
        elif power[ZERO_STATE] / base > ZERO_THRESH:
            state = ZERO_STATE
        elif power[REST_STATE] / base > RESET_FRQ_THRESH:
            state = REST_STATE
        #print (int(power0 / base), int(power1 / base), int(powerC / base))
        if len(self.audio_buffer) >= self.buf_len:
            self.audio_buffer.popleft()
        self.audio_buffer.append(state)

    def goertzel(self, frequency):
        prev1 = 0.0
        prev2 = 0.0
        norm_freq = frequency / RATE
        coeff = 2*math.cos((2*math.pi) * norm_freq)
        for sample in self.audio:
            s = sample + (coeff * prev1) - prev2
            prev2 = prev1
            prev1 = s
        power = (prev2 * prev2) + (prev1 * prev1) - (coeff * prev1 * prev2)
        return int(power) + 1  # prevents division by zero problems

    def window(self):
        WINDOW = numpy.hamming(CHUNK_SIZE)
        self.audio = [aud * win for aud, win in zip(self.audio, WINDOW)]