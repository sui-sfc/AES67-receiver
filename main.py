
import socket
import struct
'''
import pyaudio


CHUNK =1024
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=48000,
                output=True,
                frames_per_buffer=CHUNK
                )

'''
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
    #sound, address = sock.recvfrom(CHUNK*4)
    #stream.write(sound, CHUNK)
    print(RED+str(n)+END)
    n+=1

stream.close()