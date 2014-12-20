import json
from game.engine.engine import Game
from game.network.protocol import PlayerDataUnit, UserInputDataUnit
from helper.tick import TickSimulator
from logger.logger import Logger
from network.server import AbstractServerUserConnectionHandlerFactory, AbstractServerUserConnectionHandler


class ServerUserConnection():
    protocol = None
    user_id = None
    connected = False
    player = None

    def __init__(self):
        pass


class ServerUserConnectionHandlerFactory(AbstractServerUserConnectionHandlerFactory):
    def __init__(self):
        self.game = Game(Game.width, Game.height)
        self.game.init()
        self.users = {}
        self.current_id = 0

    def on_build_user_connection_handler(self):
        self.current_id += 1
        return ServerUserConnectionHandler(self.game, self.users, self.current_id)


class ServerUserConnectionHandler(AbstractServerUserConnectionHandler):

    def __init__(self, game, users, user_id):
        self.game = game
        self.user_id = user_id
        self.users = users
        self.tick_simulator = TickSimulator(Game.fps)

        connection = ServerUserConnection()
        connection.protocol = self
        connection.user_id = user_id
        self.users[self.user_id] = connection

    def on_connection_made(self):
        self.tick_simulator.simulate(self, lambda o: None)
        connection = self.users[self.user_id]
        connection.connected = True
        connection.player = self.game.add_player()

        self.update_game()

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

    def on_connection_lost(self):
        self.users[self.user_id].connected = False
        self.update_game()
        self.send_broadcast_payload({
            'type': 'lost_connection',
            'id': self.user_id
        })
        if self.user_id in self.users:
            del self.users[self.user_id]

    def on_line_received(self, json_payload):
        Logger.debug('line received: %s', json_payload, 'server')
        payload = json.loads(json_payload)

        if payload and 'type' in payload and payload['type'] == 'user_input':
            user_input = UserInputDataUnit(payload['content']).get_object()
            connection = self.users[self.user_id]
            self.game.update_player(connection.player, user_input)
            self.update_game()
            self.send_broadcast_payload_except_self({
                'type': 'user_input',
                'content': payload['content'],
                'user': PlayerDataUnit(connection.player).set_id(connection.user_id).get_pdu()
            })
        else:
            Logger.error('Unknown message type: (%s)', json_payload, 'server_protocol')


    def update_game(self):
        self.tick_simulator.simulate(self, lambda self: self.game.tick())