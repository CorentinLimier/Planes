
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory


class ClientProtocol(LineReceiver):

    def rawDataReceived(self, data):
        pass

    def __init__(self, on_new_line_callback):
        self.on_new_line_callback = on_new_line_callback

    def lineReceived(self, line):
        self.on_new_line_callback(line)


class Client(ClientFactory):
    def __init__(self, on_new_line_callback):
        self.on_new_line_callback = on_new_line_callback

    def buildProtocol(self, addr):
        return ClientProtocol(self.on_new_line_callback)


class GameClient(object):

    def __init__(self):
        self.line = 'no message'
        reactor.callLater(0.1, self.tick)

    def on_new_line_callback(self, line):
        self.line = line
        print line

    def tick(self):
        #print "tick"
        reactor.callLater(0.1, self.tick)