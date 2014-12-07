
from twisted.internet import reactor
from network.server import ServerFactory

reactor.listenTCP(5000, ServerFactory())
reactor.run()
