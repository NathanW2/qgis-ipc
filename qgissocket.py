import json
import struct
import sys
import socket
import select

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QThread, QObject, pyqtSignal

from utils import send_one_message, recv_one_message

class Worker(QObject):
    message = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.connect(('localhost', 5555))

    def run(self):
        send_one_message(self.serversocket, "Hello qgis")
        while True:
            try:
                readyread, _, _ = select.select([self.serversocket,],[], [],2)
                for client in readyread:
                    recieved = recv_one_message(client)
                    if recieved:
                        data = json.loads(recieved)
                        self.message.emit(data)

            except socket.error, msg:
                print "Socket error! %s" % msg
                break

def result(data):
    command = data["command"]
    if command == "new-layer":
        print("Making new layer...")
    elif command == "refresh-layer":
        print("Refreshing layer...")
    else:
        print("Unknown command")


thread = QThread()
worker = Worker()
worker.moveToThread(thread)

worker.message.connect(result)
thread.started.connect(worker.run)

thread.start()

from qgis.utils import iface
if not iface:
    app = QApplication([])
    app.exec_()
