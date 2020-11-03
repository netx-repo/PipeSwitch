import sys
import time
import socket

def timestamp(name, stage):
    print ('TIMESTAMP, %s, %s, %f' % (name, stage, time.time()), file=sys.stderr)

class TcpServer():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.address, self.port))
        self.sock.listen(1)

    def __del__(self):
        self.sock.close()

    def accept(self):
        conn, address = self.sock.accept()
        return conn, address


class TcpAgent:
    def __init__(self, conn):
        self.conn = conn

    def __del__(self):
        self.conn.close()

    def send(self, msg):
        self.conn.sendall(msg)

    def recv(self, msg_len):
        return self.conn.recv(msg_len, socket.MSG_WAITALL)

    def settimeout(self, t):
        self.conn.settimeout(t)


class TcpClient(TcpAgent):
    def __init__(self, address, port):
        super().__init__(None)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((address, port))