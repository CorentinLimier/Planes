
from twisted.internet import reactor
from game.network.server import ServerUserConnectionHandlerFactory

reactor.listenTCP(5000, ServerUserConnectionHandlerFactory())
reactor.run()
