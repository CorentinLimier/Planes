
import pygame
from game.engine.engine import Game
from game.hmi.hmi import Hmi
from game.network.client import ClientNetworkGameHandler
from helper.time_helpers import TickSimulator
from network.client import ClientProcessTwisted as ClientProcess
from userInputFeed.userInputFeedLocal import UserInputFeedLocal
from logger.logger import Logger

if __name__ == "__main__":
    pygame.init()
    game = Game(Game.width, Game.height)
    hmi = Hmi(game)
    clock = pygame.time.Clock()

    # init network process
    networkProcess = ClientProcess()
    networkProcess.start()

    # init local game
    localInputFeed = UserInputFeedLocal()

    # init client logic
    client_game_handler = ClientNetworkGameHandler(game)
    tick_simulator = TickSimulator(Game.fps)

    quit_the_game = False
    while not quit_the_game:
        # fetch network inputs and update game state
        if not networkProcess.output_queue.empty():
            payload = networkProcess.output_queue.get()
            Logger.debug("fetch input_queue from main, from network process to screen", category='start_client')
            client_game_handler.on_line_received(payload)

        # fetch local input and update game state
        user_input = localInputFeed.fetch_user_input()
        client_game_handler.on_local_user_input(user_input)

        # redraw game
        tick_simulator.simulate(game, lambda self: self.tick())
        #game.tick()
        hmi.draw()

        if user_input.has_pressed_something():
            # send local user_inputs
            Logger.debug("user_input to payload, from screen to network process", category='start_client')
            payload = client_game_handler.user_input_to_payload(user_input)
            Logger.trace("user_input to payload, from screen to network process: (%s)", payload, 'start_client')
            networkProcess.input_queue.put(payload)

        # ask for 60 frames per second
        clock.tick(Game.fps)

    networkProcess.stop()
    game.quit()
