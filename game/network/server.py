import json
from game.engine.engine import Game
from game.network.protocol import PlayerDataUnit, UserInputDataUnit, GameDataUnit
from helper.tick import TickSimulator
from logger.logger import Logger
from network.server import AbstractServerUserConnectionHandlerFactory, AbstractServerUserConnectionHandler


class ServerUserConnectionHandlerFactory(AbstractServerUserConnectionHandlerFactory):
    def __init__(self):
        self.game = Game(Game.width, Game.height)
        self.game.init()
        self.connections = {}
        self.current_id = 0

    def on_build_user_connection_handler(self):
        self.current_id += 1
        return ServerUserConnectionHandler(self.game, self.connections, self.current_id)


class ServerUserConnectionHandler(AbstractServerUserConnectionHandler):

    def __init__(self, game, connections, user_id):
        self.game = game
        self.user_id = user_id
        self.connections = connections
        self.tick_simulator = TickSimulator(Game.fps/2)

        self.connections[self.user_id] = self

    def on_connection_made(self):
        self.tick_simulator.simulate(self, lambda o: None)
        self.game.add_player(self.user_id)
        self.update_game()

        self.send_payload({
            'type': 'authentication',
            'user': PlayerDataUnit(self.game.get_player(self.user_id)).get_pdu(),
        })

        self.send_payload({
            'type': 'game_state_initial',
            'content': GameDataUnit(self.game).get_pdu()
        })

        self.send_broadcast_payload_except_self({
            'type': 'new_connection',
            'user': PlayerDataUnit(self.game.get_player(self.user_id)).get_pdu()
        })

    def on_connection_lost(self):
        self.update_game()
        self.send_broadcast_payload({
            'type': 'lost_connection',
            'id': self.user_id
        })
        del self.connections[self.user_id]
        self.game.remove_player(self.user_id)

    def on_line_received(self, json_payload):
        Logger.debug('line received: %s', json_payload, 'server')
        payload = json.loads(json_payload)

        if payload and 'type' in payload and payload['type'] == 'user_input':
            user_input = UserInputDataUnit(payload['content']).get_object()
            self.game.apply_user_input_to_player(self.user_id, user_input)
            self.update_game()
            self.send_broadcast_payload_except_self({
                'type': 'user_input',
                'content': payload['content'],
                'user': PlayerDataUnit(self.game.get_player(self.user_id)).get_pdu()
            })

            self.send_broadcast_payload({
                'type': 'game_state',
                'content': GameDataUnit(self.game).get_pdu()
            })
        else:
            Logger.error('Unknown message type: (%s)', json_payload, 'server_protocol')

    def update_game(self):
        self.tick_simulator.simulate(self, lambda self: self.game.tick())