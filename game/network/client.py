from game.network.protocol import UserInputDataUnit, PlayerDataUnit, GameDataUnit
from logger.logger import Logger


class ClientNetworkGameHandler():

    def __init__(self, game):
        # start the game
        game.init()

        # init local player
        self.localPlayerId = None

        # init player map
        self.playerMap = {}
        self.game = game
    
    def on_line_received(self, payload):
        if payload and 'type' in payload:
            if payload['type'] == 'user_input':
                Logger.trace("fetch input_queue from main, from network process to screen: (%s)", payload, 'client_protocol')
                user_input = UserInputDataUnit(payload['content']).get_object()
                user_id = payload['user']['id']
                self.game.apply_user_input_to_player(user_id, user_input)

            elif payload['type'] == 'authentication':
                Logger.info("Authentication (%s)", payload, 'client_protocol')
                self.localPlayerId = payload['user']['id']
                self.game.add_player(self.localPlayerId)

            elif payload['type'] == 'game_state_initial':
                Logger.info("Game state initial (%s)", payload, 'client_protocol')
                for user_pdu in GameDataUnit(payload['content']).get_players_pdu():
                    if not user_pdu.get_id() == self.localPlayerId:
                        player = self.game.add_player(user_pdu.get_id())
                        player.set_position(user_pdu.get_position())

            elif payload['type'] == 'game_state':
                Logger.info("Game state (%s)", payload, 'client_protocol')
                for user_pdu in GameDataUnit(payload['content']).get_players_pdu():
                    player = self.game.get_player(user_pdu.get_id())
                    player.set_position(user_pdu.get_position())

            elif payload['type'] == 'new_connection':
                Logger.info("User new connection (%s)", payload, 'client_protocol')
                user_id = payload['user']['id']
                self.game.add_player(user_id)

            elif payload['type'] == 'lost_connection':
                Logger.info("User lost connection (%s)", payload, 'client_protocol')
                user_id = payload['id']
                self.game.remove_player(user_id)

            else:
                Logger.error('Unknown payload type: (%s)', payload['type'], 'client_protocol')

        else:
            Logger.error('Payload not defined or "type" key not defined: %s', payload, 'client_protocol')

    def on_local_user_input(self, user_input):
        if self.localPlayerId is not None:
            self.game.apply_user_input_to_player(self.localPlayerId, user_input)

    def user_input_to_payload(self, user_input):
        return {
            'type': 'user_input',
            'content': UserInputDataUnit(user_input).get_pdu()
        }