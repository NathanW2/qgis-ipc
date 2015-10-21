import struct
import socket
import json

from utils import recv_one_message, send_one_message

port = 5555
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('localhost', port))
socket.listen(1) # become a server socket, maximum 5 connections

# block for connection
print("Waiting for connection from client...")
client, addr = socket.accept()

print("Got connection to {}".format(client))

# Got a hello world
recieved = recv_one_message(client)
if recieved == "Hello qgis":
    print("Got hello message {}".format(recieved))
    print("Sending some commands now..")

    data = dict(command="new-layer",
                name="my layer",
                type="point"
                )
    send_one_message(client, data)

    data = dict(command="refresh-layer")
    send_one_message(client, data)

    data = dict(command="other")
    send_one_message(client, data)

    # Send more commands.

# We just wait here until we are killed.
while True:
    pass

import atexit

def cleanup():
    # shutdown the socket
    try:
        socket.shutdown(socket.SHUT_RDWR)
    except:
        pass

    socket.close()

atexit.register(cleanup)

