# Audio constants
RATE = 44100
CHUNK_SIZE = 512
AUDIOBUF_SIZE = 2048

# Constants for FSK
BASE_FRQ=   18600.0
RESET_FRQ=  18800.0
ZERO_FRQ=   19000.0
ONE_FRQ=    19200.0
TWO_FRQ=    19400.0
THREE_FRQ=  19600.0
FOUR_FRQ=   19800.0
FIVE_FRQ=   20000.0
SIX_FRQ=    20200.0
SEVEN_FRQ=  20400.0
EIGHT_FRQ=  20600.0
NINE_FRQ=   20800.0

RESET_FRQ_THRESH = 100
ZERO_THRESH=    100
ONE_THRESH=     100
TWO_THRESH=     100
THREE_THRESH=   100
FOUR_THRESH=    100
FIVE_THRESH=    100
SIX_THRESH=     100
SEVEN_THRESH=   100
EIGHT_THRESH=   100
NINE_THRESH=    100


STATES= 12 #include reset and base states
ZERO_STATE=  0
ONE_STATE =  1
TWO_STATE =  2
THREE_STATE= 3
FOUR_STATE = 4
FIVE_STATE = 5
SIX_STATE =  6
SEVEN_STATE= 7
EIGHT_STATE= 8
NINE_STATE=  9
REST_STATE = STATES-2
UNDEFINED_STATE = STATES-1

BIT_DURATION = 0.2
IDLE_LIMIT = 20 #If we don't hear anything for a while (~2sec), clear buffer.
RECV_TIMEOUT = 120 #In sec
VICTIM_AUD_FILE = '/home/ofir/Desktop/AudioAlpha/tests/victimAudio'