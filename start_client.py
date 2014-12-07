
from twisted.internet import reactor
from network.client import GameClient, Client


if __name__ == '__main__':
    game_client = GameClient()
    reactor.connectTCP('127.0.0.1', 5000, Client(game_client.on_new_line_callback))
    reactor.run()



