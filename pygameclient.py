
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from game.engine.engine import Game

'''
class GameClientProtocol(LineReceiver):

    def rawDataReceived(self, data):
        pass

    def __init__(self, recv):
        self.recv = recv

    def lineReceived(self, line):
        self.recv(line)


class GameClient(ClientFactory):
    def __init__(self, recv):
        self.protocol = GameClientProtocol
        self.recv = recv

    def buildProtocol(self, addr):
        return GameClientProtocol(self.recv)


class Client(object):

    def __init__(self):
        self.game = Game()
        self.line = 'no message'
        reactor.callLater(0.1, self.tick)

    def new_line(self, line):
        self.line = line

    def tick(self):
        self.game.tick()
        reactor.callLater(0.1, self.tick)
'''


#if __name__ == '__main__':

#    client = Client()
#    reactor.connectTCP('127.0.0.1', 5000, GameClient(client.new_line))
#    reactor.run()



if __name__ == "__main__":
    import pygame
    pygame.init()
    game = Game()
    clock = pygame.time.Clock()

    game.init()

    while game.tick():
        # frames per seconds
        clock.tick(60)

    game.quit()