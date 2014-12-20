from userInput.userInput import UserInput


class Serializer():

    def __init__(self):
        pass

    @staticmethod
    def user_input_to_payload(user_input):
        payload = {
            'has_pressed_left': user_input.has_pressed_left,
            'has_pressed_right': user_input.has_pressed_right
        }
        return payload

    @staticmethod
    def payload_to_user_input(payload):
        user_input = UserInput()
        user_input.has_pressed_left = payload['content']['has_pressed_left']
        user_input.has_pressed_right = payload['content']['has_pressed_right']
        return user_input

    @staticmethod
    def connection_to_player_definition_dic(connection):
        return {
            'id': connection.id,
            'position': connection.player.get_position()
        }