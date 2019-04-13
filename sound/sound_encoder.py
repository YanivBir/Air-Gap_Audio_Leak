import wave

import numpy as np
import pyaudio
from scipy.io import wavfile
from sound.sound_constants import *
from packet.packet_constants import *
from packet.audio_packet import *
from sound.sound_decoder import *

class Encoder:
    def __init__(self):
        #self.num_channels = 1      #unused
        #self.bits_per_sample = 16  #unused
        #self.amplitude = 0.5       #unused
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  output=True,
                                  frames_per_buffer=AUDIOBUF_SIZE)

    def string2sound(self, binform):
        #print('binform : ' + binform)
        soundlist = []
        for b in binform:
            if (b is '0'):
                freq = ZERO_FRQ
            elif (b is '1'):
                freq = ONE_FRQ
            elif (b is '2'):
                freq = TWO_FRQ
            elif (b is '3'):
                freq = THREE_FRQ
            elif (b is '4'):
                freq = FOUR_FRQ
            elif (b is '5'):
                freq = FIVE_FRQ
            elif (b is '6'):
                freq = SIX_FRQ
            elif (b is '7'):
                freq = SEVEN_FRQ
            elif (b is '8'):
                freq = EIGHT_FRQ
            elif (b is '9'):
                freq = NINE_FRQ
            elif (b is PACKET_RESET_SYMBOL):
                freq = RESET_FRQ
            else:
                print('wrong value')
            soundlist = np.hstack((soundlist, self.getbit(freq)))
        return soundlist

    # def encode2wav(self, somestring, filename):
    #     soundlist = self.string2sound(somestring)
    #     wavfile.write(filename, RATE, soundlist.astype(np.dtype('int16')))

    def encodeplay(self, somestring, filename):
        soundlist = self.string2sound(somestring)
        wavfile.write(filename, RATE, soundlist.astype(np.dtype('int16')))
        # self.stream.write(soundlist.astype(np.dtype('int16')))

        # open the file for reading.
        wf = wave.open(filename, 'rb')

        # create an audio object
        p = pyaudio.PyAudio()

        # open stream based on the wave object which has been input.
        stream = p.open(format=
                        p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        frames_per_buffer=AUDIOBUF_SIZE)

        # read data (based on the chunk size)
        data = wf.readframes(CHUNK_SIZE)

        # play stream (looping from beginning of file to the end)
        while data != b'':
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(CHUNK_SIZE)

        stream.write(data)

        # cleanup stuff.
        stream.stop_stream()
        stream.close()
        p.terminate()

    def send (self, packet, soundRecv):
        print('send packet type: ' + str(packet.type) + ' seq: ' + str(packet.seq))
        soundRecv.stop_listening()
        self.encodeplay(packet.toString(), VICTIM_AUD_FILE)
        soundRecv.start_listening()

    def getbit(self, freq):
        music = []
        t = np.arange(0, BIT_DURATION, 1. / RATE)  # time
        x = np.sin(2 * np.pi * freq * t)  # generated signals
        x = [int(val * 32000) for val in x]
        sigmoid = [1 / (1 + np.power(np.e, -t)) for t in np.arange(-6, 6, 0.01)]
        sigmoid_inv = sigmoid[::-1]
        xstart = len(x) - len(sigmoid)
        for i in range(len(sigmoid)):
            x[xstart + i] = x[xstart + i] * sigmoid_inv[i]
            x[i] = x[i] * sigmoid[i]
        music = np.hstack((music, x))
        return music

    def quit(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()