from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
import json
from logger.logger import Logger


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
            'type': 'authentication',
            'content': json.dumps({'id': self.id})
        })
        self.send_payload({
            'id': self.id,
            'type': 'user_list',
            'users': json.dumps({'ids': self.users.keys()})
        })

    def connectionLost(self, reason):
        self.users[self.id].connected = False
        self.send_broadcast_payload({
            'id': self.id,
            'type': 'server_message',
            'content': 'disconnected'
        })
        if self.id in self.users:
            del self.users[self.id]

    def lineReceived(self, json_payload):
        Logger.debug('line received: %s', json_payload, 'server')
        payload = json.loads(json_payload)
        self.send_broadcast_payload_except_self({
            'id': self.id,
            'type': 'user_input',
            'content': payload
        })

    def send_broadcast_payload_except_self(self, payload):
        payload = json.dumps(payload)
        Logger.debug('broadcasting except self: %s', payload, 'server')
        for name, connection in self.users.iteritems():
            if connection.protocol != self:
                connection.protocol.sendLine(payload)

    def send_broadcast_payload(self, payload):
        payload = json.dumps(payload)
        Logger.debug('broadcasting to all: %s', payload, 'server')
        for name, connection in self.users.iteritems():
            connection.protocol.sendLine(payload)

    def send_payload(self, payload):
        payload = json.dumps(payload)
        Logger.debug('send payload to self only: %s', payload, 'server')
        self.sendLine(payload)

    def rawDataReceived(self, data):
        LineReceiver.rawDataReceived(self, data)


class ServerFactory(Factory):

    def __init__(self):
        self.users = {}
        self.current_id = 0

    def buildProtocol(self, address):
        self.current_id += 1
        return ConnectionHandler(self.users, self.current_id)
