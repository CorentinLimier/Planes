

from game.bo.plane import Plane


class Player():

    def __init__(self, game, input_feed):
        self.game = game
        self.input_feed = input_feed
        self.plane_xy = (self.game.display_width * 0.45, self.game.display_height * 0.8)
        self.plane_crashed = False

    def update_state_from_input_feed(self):
        user_input = self.input_feed.fetch_user_input()
        self.plane_xy = (self.plane_xy[0], self.plane_xy[1] + user_input.orientation_delta)
        if user_input.has_pressed_quit:
            self.plane_crashed = True
