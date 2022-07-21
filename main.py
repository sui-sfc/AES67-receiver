from os import TMP_MAX
import threading
import socket
import struct
from tarfile import CHRTYPE
import pyaudio
from requests import NullHandler


class RingBuffer:
    def __init__(self, size):
        self.buffer = [None for i in range(0, size)]
        self.top = 0
        self.bottom = 0
        self.size = size

    def __len__(self):
        return self.bottom - self.top

    def add(self, value):
        self.buffer[self.bottom] = value
        self.bottom = (self.bottom + 1) % len(self.buffer)

    def get(self, index=None):
        if index is not None:
            return self.buffer[index]

        value = self.buffer[self.top]
        self.top = (self.top + 1) % len(self.buffer)
        return value


def RTPSTRIP(data):
    return (bytearray(data)[12:])

def receive():
    print('receive')
    MCAST_GRP = '239.69.138.19'
    MCAST_PORT = 5004

    sock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM,
                        socket.IPPROTO_UDP
                        )

    sock.setsockopt(socket.SOL_SOCKET,
                    socket.SO_REUSEADDR,
                    1
                    )

    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    data, address = sock.recvfrom(1280)
    global n
    print('data====================')
    print(data.hex())
    print('sound====================')
    print(RTPSTRIP(data).hex())
    while True:
        sound=b''
        for i in range(8):
            data, address = sock.recvfrom(1280+32)
            sound+=RTPSTRIP(data)
        rbuf.add(sound)
        n=2

def a_play():
    global n
    print('a_play')
    CHUNK = 288
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt24,
                    channels=2,
                    rate=48000,
                    output=True,
                    frames_per_buffer=CHUNK
                    )
    while True:
        try:
            sound = rbuf.get()
            if n > 1:
                print(len(sound))
                stream.write(bytes(sound),CHUNK)
                
        except:
            pass

'''
data, address = sock.recvfrom(CHUNK)
print(RED+'data'+END)
print(data)
print(RED+'bytearray'+END)
sound = bytearray(data)[12:]
'''


if __name__ == '__main__':
    #48*24*2
    global sound,n
    n = 0
    r_CHUNK = 288*4
    rbuf = RingBuffer(16)
    n = 0
    RED = '\033[31m'
    END = '\033[0m'
    print(RED+'Streaming'+END)
    thread1 = threading.Thread(target=receive)
    thread2 = threading.Thread(target=a_play)
    thread1.start()
    thread2.start()
