from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
import json


class Connection():
    protocol = None
    id = None
    connected = False

    def __init__(self):
        pass


class ConnectionHandler(LineReceiver):

    def __init__(self, users, id):
        self.users = users
        self.id = id

        connexion = Connection()
        connexion.protocol = self
        self.users[self.id] = connexion

    def connectionMade(self):
        self.users[self.id].connected = True
        self.users[self.id].id = True
        self.send_broadcast_payload({
            'id': self.id,
            'line': 'connected'
        })

    def connectionLost(self, reason):
        self.users[self.id].connected = False
        self.send_broadcast_payload({
            'id': self.id,
            'line': 'disconnected'
        })
        if self.id in self.users:
            del self.users[self.id]

    def lineReceived(self, line):
        self.send_broadcast_payload({
            'id': self.id,
            'line': line
        })

    def send_broadcast_payload_except_self(self, payload):
        print "broadcast except: %s" % json.dumps(payload)
        for name, connection in self.users.iteritems():
            if connection.protocol != self:
                connection.protocol.sendLine(json.dumps(payload))

    def send_broadcast_payload(self, payload):
        print "broadcast: %s" % json.dumps(payload)
        for name, connection in self.users.iteritems():
            connection.protocol.sendLine(json.dumps(payload))

    def send_payload(self, payload):
        print "send: %s" % json.dumps(payload)
        self.sendLine(json.dumps(payload))

    def rawDataReceived(self, data):
        pass


class ServerFactory(Factory):

    def __init__(self):
        self.users = {}
        self.current_id = 0

    def buildProtocol(self, address):
        self.current_id += 1
        return ConnectionHandler(self.users, self.current_id)
