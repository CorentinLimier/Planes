
from twisted.internet import reactor
from network.client import ClientFactory

class GameClient(object):

    def __init__(self):
        reactor.callLater(0.1, self.tick)

    def on_new_line_callback(self, line):
        self.line = line
        print line

    def tick(self):
        #print "tick"
        reactor.callLater(0.1, self.tick)

class GameServer(object):

    def __init__(self):
        reactor.callLater(0.1, self.tick)

    def on_new_line_callback(self, line):
        self.line = line
        print line

    def tick(self):
        reactor.callLater(0.1, self.tick)


if __name__ == '__main__':
    game_client = GameClient()
    reactor.connectTCP('127.0.0.1', 5000, ClientFactory(game_client.on_new_line_callback))
    reactor.run()

