from struct import unpack
from audioop import add
import socket
import struct
from unittest import skip
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum
import sounddevice as sd
import numpy as np

class RtpPacket(KaitaiStruct):
    
    class PayloadTypeEnum(Enum):

        pcm = 36
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.version = self._io.read_bits_int_be(2)
        self.has_padding = self._io.read_bits_int_be(1) != 0
        self.has_extension = self._io.read_bits_int_be(1) != 0
        self.csrc_count = self._io.read_bits_int_be(4)
        self.marker = self._io.read_bits_int_be(1) != 0
        self.payload_type = KaitaiStream.resolve_enum(
            RtpPacket.PayloadTypeEnum, self._io.read_bits_int_be(7))
        self._io.align_to_byte()
        self.sequence_number = self._io.read_u2be()
        self.timestamp = self._io.read_u4be()
        self.ssrc = self._io.read_u4be()
        if self.has_extension:
            self.header_extension = RtpPacket.HeaderExtention(
                self._io, self, self._root)

        self.data = self._io.read_bytes(
            ((self._io.size() - self._io.pos()) - self.has_padding))
        self.padding = self._io.read_bytes(self.has_padding)

    class HeaderExtention(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.id = self._io.read_u2be()
            self.length = self._io.read_u2be()


interface = 'en6'
CHUNK = 48*24
#1152
MCAST_GRP = '239.69.138.19'
MCAST_PORT = 5004
ETH_P_ALL = 3
sd.default.samplerate = 48000  # サンプリングレート
sd.default.channels = 2  # チャネル数

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
n = 0

RED='\033[31m'
END='\033[0m'


sound = b''
i=0
n=0



tmp, address = sock.recvfrom(288*4)
data = RtpPacket(KaitaiStream(BytesIO(tmp)))
#stream.write(sound)
print(address)


while True:
    tmp, address = sock.recvfrom(CHUNK*4)
    data = RtpPacket(KaitaiStream(BytesIO(tmp)))
    sound = data.data
    
    read_frames = len(sound)
    nbyte = 3
    data = [unpack("<i",
            bytearray([0]) + sound[nbyte * idx:nbyte * (idx + 1)])[0]
            for idx in range(read_frames)]
    sound = np.array(data, dtype='int16')
    sd.play(sound)
    #'''
    n+=1
    


    
stream.close()
