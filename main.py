
import socket
import struct
MCAST_GRP = '239.69.249.134'
MCAST_PORT = 5004
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
n = 0

RED='\033[31m'
END='\033[0m'

while True:
    print(RED+str(n)+END)
    print(sock.recv(1024))
    n+=1

'''
from socket import socket, AF_INET, SOCK_DGRAM
#import pyaudio
import wave
import sys

CHUNK = 1024
HOST = ''
PORT = 319


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                output=True,
                frames_per_buffer=CHUNK
                )

s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))

sound, address = s.recvfrom(CHUNK*4)

print('nowplaying from ' + str(address))
while sound != b'':
    #stream.write(sound, CHUNK)
    sound, address = s.recvfrom(CHUNK*4)

print('stop')
#stream.close()
s.close()
'''