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

    def from_object(self, player):
        self.pdu = {
            'position': player.get_position()
        }
        return self

    def set_id(self, user_id):
        self.pdu['id'] = user_id
        return self

    def get_object(self):
        player = Player()
        player.set_position(self.pdu['position'])
        return player

    def get_pdu(self):
        return self.pdu

