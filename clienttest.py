
import sys
import socket


from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from multiprocessing import Pool


def normalClient():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5006
    BUFFER_SIZE = 1024

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((TCP_IP, TCP_PORT))

    while True:
        userInput = raw_input('Enter smth: ')
        if userInput == 'quit':
            socket.send('quit')
            socket.close()
            break
        socket.send(userInput)
        data = socket.recv(BUFFER_SIZE)
        print "received data:", data

def broadcastClient():
    MYPORT = 50000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 0))

    while 1:
        print "recv"
        data, wherefrom = s.recvfrom(1500, 0)
        print data
        print wherefrom





class EchoClient(LineReceiver):
    end="Bye-bye!"
    def connectionMade(self):
        self.sendLine("Hello, world!")
        self.sendLine("What a fine day it is.")
        self.sendLine(self.end)

    def lineReceived(self, line):
        print "receive:", line
        if line==self.end:
            self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()


def aSillyBlockingMethod():
    while True:
        userInput = raw_input('Enter smth: ')
        if userInput == 'quit':
            socket.send('quit')
            socket.close()
            break
        socket.send(userInput)
        data = socket.recv(1024)
        print "received data:", data

def twistedClient():
    factory = EchoClientFactory()
    reactor.connectTCP('localhost', 5000, factory)
    reactor.callInThread(aSillyBlockingMethod, "2 seconds have passed")
    reactor.run()

print "twisted client starting"
twistedClient()
print "twisted client started"
