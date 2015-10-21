# QGIS IPC

Some random stuff on doing IPC between QGIS and another application using sockets.

Nothing too fancy.

- `server.py` - Goes into the application that needs to talk to QGIS.
- `qgissocket.py` - Creates a socket connection to the send and waits for commands.

The QGIS side is all done in a thread to avoid blocking anything and passes the messages out
via a singal for more work.