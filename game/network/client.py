from game.network.protocol import UserInputDataUnit, PlayerDataUnit
from logger.logger import Logger


class ClientNetworkGameHandler():

    def __init__(self, game):
        # start the game
        game.init()

        # init local player
        self.localPlayerId = None
        self.localPlayer = game.add_player()

        # init player map
        self.playerMap = {}
        self.game = game
    
    def on_line_received(self, payload):
        if payload and 'type' in payload:
            if payload['type'] == 'user_input':
                Logger.trace("fetch input_queue from main, from network process to screen: (%s)", payload, 'client_protocol')
                user_input = UserInputDataUnit(payload['content']).get_object()
                user_id = payload['user']['id']
                self.game.update_player(self.playerMap[user_id], user_input)

            elif payload['type'] == 'authentication':
                Logger.info("Authentication (%s)", payload, 'client_protocol')
                self.localPlayerId = payload['user']['id']
                self.playerMap[self.localPlayerId] = self.localPlayer

            elif payload['type'] == 'user_list':
                Logger.info("User list (%s)", payload, 'client_protocol')
                for user_pdu in payload['users']:
                    if not user_pdu['id'] == self.localPlayerId:
                        network_player = self.game.add_player(PlayerDataUnit(user_pdu).get_object().get_position())
                        self.playerMap[user_pdu['id']] = network_player

            elif payload['type'] == 'new_connection':
                Logger.info("User new connection (%s)", payload, 'client_protocol')
                user_id = payload['user']['id']
                network_player = self.game.add_player()
                self.playerMap[user_id] = network_player

            elif payload['type'] == 'lost_connection':
                Logger.info("User lost connection (%s)", payload, 'client_protocol')
                user_id = payload['id']
                self.game.remove_player(self.playerMap[user_id])
                self.playerMap.pop(user_id, None)

            else:
                Logger.error('Unknown payload type: (%s)', payload['type'], 'client_protocol')

        else:
            Logger.error('Payload not defined or "type" key not defined: %s', payload, 'client_protocol')

    def on_local_user_input(self, user_input):
        self.game.update_player(self.localPlayer, user_input)

    def user_input_to_payload(self, user_input):
        return {
            'type': 'user_input',
            'content': UserInputDataUnit(user_input).get_pdu()
        }