import struct
import socket
import json
import time

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
                type="Point?crs=epsg:4326"
                )
    send_one_message(client, data)

    time.sleep(1.2)
    data = dict(command="other")
    send_one_message(client, data)

    time.sleep(1.2)
    data = dict(command="new-layer",
                name="my layer 2",
                type="Linestring?crs=epsg:4326"
    )
    send_one_message(client, data)

try:
    socket.shutdown(socket.SHUT_RDWR)
except:
    pass

socket.close()

