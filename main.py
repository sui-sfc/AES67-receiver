
import socket
import struct
from unittest import skip
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


import pyaudio
CHUNK = 1024

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt24,
                channels=1,
                rate=48000,
                output=True,
                frames_per_buffer=CHUNK
                )


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


class RtpPacket(KaitaiStruct):
    
    class PayloadTypeEnum(Enum):
        pcmu = 0
        reserved1 = 1
        reserved2 = 2
        gsm = 3
        g723 = 4
        dvi4_1 = 5
        dvi4_2 = 6
        lpc = 7
        pcma = 8
        g722 = 9
        l16_1 = 10
        l16_2 = 11
        qcelp = 12
        cn = 13
        mpa = 14
        g728 = 15
        dvi4_3 = 16
        dvi4_4 = 17
        g729 = 18
        reserved19 = 19
        unassigned20 = 20
        unassigned21 = 21
        unassigned22 = 22
        unassigned23 = 23
        unassigned24 = 24
        celb = 25
        jpeg = 26
        unassigned27 = 27
        nv = 28
        unassigned29 = 29
        unassigned30 = 30
        h261 = 31
        mpv = 32
        mp2t = 33
        h263 = 34
        pcm = 36
        mpeg_ps = 96
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

while True:
    sound,address = sock.recvfrom(CHUNK)
    data = RtpPacket(KaitaiStream(BytesIO(sound)))
    print(RED+str(address)+END)
    print(sound)
    print(data.data)
    #stream.write(data.data, CHUNK*4)

stream.close()