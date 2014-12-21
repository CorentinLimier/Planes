from game.bo.player import Player
from network.application import ProtocolDataUnit
from userInput.userInput import UserInput


class UserInputDataUnit(ProtocolDataUnit):

    def from_object(self, user_input):
        self.pdu = {
            'has_pressed_left': user_input.has_pressed_left,
            'has_pressed_right': user_input.has_pressed_right,
            'has_pressed_fire': user_input.has_pressed_fire
        }
        return self

    def get_object(self):
        user_input = UserInput()
        user_input.has_pressed_left = self.pdu['has_pressed_left']
        user_input.has_pressed_right = self.pdu['has_pressed_right']
        user_input.has_pressed_fire = self.pdu['has_pressed_fire']
        return user_input

    def get_pdu(self):
        return self.pdu


class PlayerDataUnit(ProtocolDataUnit):

    def __init__(self, pdu_or_object, user_id=None):
        self.pdu = {}
        if isinstance(pdu_or_object, dict):
            self.from_dictionary(pdu_or_object)
        else:
            self.from_object(pdu_or_object, user_id)

    def from_object(self, player, user_id):
        self.pdu = {
            'position': player.get_position(),
            'id': user_id
        }
        return self

    def get_id(self):
        return self.pdu['id']

    def get_position(self):
        return self.pdu['position']

    def get_pdu(self):
        return self.pdu


class GameDataUnit(ProtocolDataUnit):

    def __init__(self, pdu_or_object, player_map=None):
        self.pdu = {}
        if isinstance(pdu_or_object, dict):
            self.from_dictionary(pdu_or_object)
        else:
            self.from_object(pdu_or_object, player_map)

    def from_object(self, game, player_map):
        self.pdu = {
            'width': game.width,
            'height': game.height,
            'fps': game.fps,
            'default_position': game.default_position,
            'players': []
        }
        for user_id, player in enumerate(player_map):
            self.pdu['players'].append(PlayerDataUnit(player, user_id).get_pdu())
        return self

    def from_dictionary(self, dictionary):
        players_pdu = []
        for player in dictionary['players']:
            players_pdu.append(PlayerDataUnit(player))
        dictionary['players'] = players_pdu
        self.pdu = dictionary

    def get_players_pdu(self):
        return self.pdu['players']

    def get_pdu(self):
        return self.pdu

