import socket


class Server():

    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 5005
        self.bufferSize = 20
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.bind((self.ip, self.port))

    def getLastInput(self):
        while 1:
            yield s.recv(BUFFER_SIZE)

        