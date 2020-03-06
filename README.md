# Air-Gap-Audio-Leak


Project Goal: Leaking data from an air-Gap network to an open network, by using ultrasonic waves as an alternative communication channel.

The Ultrasonic communication is via a covert channel.
It sends and receives data using the standard built-in laptop microphone and speakers.

* The pure victim data is encoded by Huffman encoder and inserted to a DATA packet.

* Error detection is achieved using the BSD checksum algorithm.

* Reliable data transfer is achieved by implementing: Stop and Wait Protocol using three types of packets DATA, ACK and FIN.

* Encoding to sound is by a Frequency Shift Keying scheme wherein each digit value is represented by a specific frequency (18800Hz to 20800Hz).

**Project Architecture**

|Pure data|<--->|Huffman En/Decoder|<---> |Build packet|<---> |Calc BSD checksum|  <---> |Sound En/Decoder|
