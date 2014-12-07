import socket
import select
import time

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


def normalServer():
    host = '127.0.0.1'
    port = 5006
    backlog = 5
    size = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(backlog)
    clients = [s]

    while 1:
      inputReady, outputReady, exceptReady = select.select(clients, [], [])
      for x in inputReady:

        if x == s:
            csock, addr = s.accept()
            clients.append(csock)

        else:
            data = x.recv(size)
            print data
            if data:
                if data == 'quit':
                    exit()
                x.send(data)
            else:
                x.close()
                clients.remove(x)
    s.close()

def broadcastServer():
    MYPORT = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('', 0))

    while 1:
        data = repr(time.time()) + '\n'
        s.sendto(data, ('<broadcast>', MYPORT))
        print data
        time.sleep(1)


class Chat(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine("What's your name?")

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if self.users.has_key(name):
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):

    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)


def twistedServer():
    reactor.listenTCP(5000, ChatFactory())
    reactor.run()

twistedServer()