

from game.bo.plane import Plane


class Player():

    def __init__(self, game, hmi):
        self.game = game
        self.hmi = hmi
        self.plane = Plane((self.hmi.width * 0.45, self.hmi.height * 0.8), 0)


    def update_state(self, user_input):
        if user_input:
            orientation_delta = 0
            if user_input.has_pressed_left:
                orientation_delta = -5
            elif user_input.has_pressed_right:
                orientation_delta = 5

            self.plane.position = (self.plane.position[0], self.plane.position[1] + orientation_delta)
            if user_input.has_pressed_quit:
                self.plane.crashed = True
