import json
import struct

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def send_one_message(sock, data):
    if isinstance(data, dict):
        data = json.dumps(data)
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)
