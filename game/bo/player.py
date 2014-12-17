
from userInput.userInput import UserInput, UserInputAggregate
from game.bo.plane import Plane


class Player():

    def __init__(self, game):
        self.game = game
        self.plane = Plane(game)

    def update_state(self, user_input):
                
        if user_input:
            if isinstance(user_input, UserInput):
                if user_input.has_pressed_left:
                    self.plane.turn_left()
                elif user_input.has_pressed_right:
                    self.plane.turn_right()
                if user_input.has_pressed_quit:
                    self.plane.crash()

            elif isinstance(user_input, UserInputAggregate):
                if user_input.pressed_left_frame_count:
                    self.plane.turn_left(user_input.pressed_left_frame_count)
                elif user_input.pressed_right_frame_count:
                    self.plane.turn_right(user_input.pressed_right_frame_count)
            else:
                raise Exception('Not implemented user input type %s(%s)' % (type(user_input), user_input))


    def get_position(self):
        return self.plane.position

    def set_position(self, position):
        self.plane.position = position
        return self