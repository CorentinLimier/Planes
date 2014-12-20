import time
from twisted.internet.protocol import Factory, connectionDone
from twisted.protocols.basic import LineReceiver
import json
from logger.logger import Logger


class AbstractServerUserConnectionHandler(LineReceiver):

    def __init__(self):
        pass

    def connectionMade(self):
        return self.on_connection_made()

    def connectionLost(self, reason=connectionDone):
        self.on_connection_lost()
        return reason

    def lineReceived(self, json_payload):
        return self.on_line_received(json_payload)

    def on_line_received(self, json_payload):
        raise NotImplementedError('on_line_received')

    def on_connection_lost(self):
        raise NotImplementedError('on_connection_lost')

    def on_connection_made(self):
        raise NotImplementedError('on_connection_made')

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


class AbstractServerUserConnectionHandlerFactory(Factory):

    def __init__(self):
        pass

    def buildProtocol(self, address):
        return self.on_build_user_connection_handler()

    def on_build_user_connection_handler(self):
        raise NotImplementedError('on_build_user_connection_handler')
