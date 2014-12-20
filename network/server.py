from twisted.internet.protocol import Factory, connectionDone
from twisted.protocols.basic import LineReceiver
import json
from game.network.protocol import PlayerDataUnit, UserInputDataUnit
from logger.logger import Logger
from game.engine.engine import Game


class Connection():
    protocol = None
    user_id = None
    connected = False
    player = None

    def __init__(self):
        pass


class ConnectionHandler(LineReceiver):

    def __init__(self, game, users, user_id):
        self.users = users
        self.user_id = user_id
        self.game = game

        connection = Connection()
        connection.protocol = self
        connection.user_id = user_id
        self.users[self.user_id] = connection

    def connectionMade(self):
        connection = self.users[self.user_id]
        connection.connected = True
        connection.player = self.game.add_player()

        self.send_payload({
            'type': 'authentication',
            'user': PlayerDataUnit(connection.player).set_id(connection.user_id).get_pdu(),
        })

        user_list = []
        for connection in self.users.itervalues():
            user_list.append(PlayerDataUnit(connection.player).set_id(connection.user_id).get_pdu())

        self.send_payload({
            'type': 'user_list',
            'users': user_list
        })

        self.send_broadcast_payload_except_self({
            'type': 'new_connection',
            'user': PlayerDataUnit(connection.player).set_id(connection.user_id).get_pdu()
        })

    def connectionLost(self, reason=connectionDone):
        self.users[self.user_id].connected = False
        self.send_broadcast_payload({
            'type': 'lost_connection',
            'id': self.user_id
        })
        if self.user_id in self.users:
            del self.users[self.user_id]
        return reason

    def lineReceived(self, json_payload):
        Logger.debug('line received: %s', json_payload, 'server')
        payload = json.loads(json_payload)

        if payload and 'type' in payload and payload['type'] == 'user_input':
            user_input = UserInputDataUnit(payload['content']).get_object()
            connection = self.users[self.user_id]
            self.game.update_player(connection.player, user_input)
            self.send_broadcast_payload_except_self({
                'type': 'user_input',
                'content': payload['content'],
                'user': PlayerDataUnit(connection.player).set_id(connection.user_id).get_pdu()
            })
        else:
            Logger.error('Unknown message type: (%s)', json_payload, 'server')

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
        self.game = Game(800, 400)
        self.users = {}
        self.current_id = 0

    def buildProtocol(self, address):
        self.current_id += 1
        return ConnectionHandler(self.game, self.users, self.current_id)
