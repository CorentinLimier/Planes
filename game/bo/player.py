

from game.bo.plane import Plane


class Player():

    def __init__(self, game):
        self.game = game
        self.plane_xy = (self.game.display_width * 0.45, self.game.display_height * 0.8)
        self.plane_crashed = False

    def update_state(self, user_input):
        if user_input:
            self.plane_xy = (self.plane_xy[0], self.plane_xy[1] + user_input.orientation_delta)
            if user_input.has_pressed_quit:
                self.plane_crashed = True
