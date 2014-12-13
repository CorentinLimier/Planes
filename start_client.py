
import pygame
from game.engine.engine import Game
from game.bo.player import Player
from network.client import ClientProcessTwisted as ClientProcess
from userInputFeed.userInputFeedLocal import UserInputFeedLocal
from userInput.userInput import UserInput
from logger.logger import Logger

if __name__ == "__main__":
    pygame.init()
    game = Game()
    clock = pygame.time.Clock()

    networkProcess = ClientProcess()
    networkProcess.start()

    localInputFeed = UserInputFeedLocal()

    game.init()
    localPlayer = Player(game)
    networkPlayer = Player(game)
    game.add_player(localPlayer)
    game.add_player(networkPlayer)

    def user_input_to_payload(user_input):
        payload = {}
        payload['has_pressed_left'] = user_input.has_pressed_left
        payload['has_pressed_right'] = user_input.has_pressed_right
        return payload

    def payload_to_user_input(payload):
        user_input = UserInput()
        user_input.has_pressed_left = payload['content']['has_pressed_left']
        user_input.has_pressed_right = payload['content']['has_pressed_right']
        return user_input


    quit = False
    while not quit:
        # fetch network inputs and update game state
        if not networkProcess.output_queue.empty():
            payload = networkProcess.output_queue.get()
            Logger.debug("fetch input_queue from main, from network process to screen", category='start_client')

            if payload and 'type' in payload and payload['type'] == 'user_input':
                Logger.trace("fetch input_queue from main, from network process to screen: (%s)", payload, 'start_client')
                user_input = payload_to_user_input(payload)
                networkPlayer.update_state(user_input)

            if payload and 'type' in payload and payload['type'] == 'authentication':
                pass

            if payload and 'type' in payload and payload['type'] == 'user_list':
                pass

        # fetch local input and update game state
        user_input = localInputFeed.fetch_user_input()
        localPlayer.update_state(user_input)

        # check for quit button
        if localPlayer.plane_crashed or networkPlayer.plane_crashed:
            quit = True

        # redraw game
        game.draw()

        # send local user_inputs
        Logger.debug("user_input to payload, from screen to network process", category='start_client')
        payload = user_input_to_payload(user_input)
        Logger.trace("user_input to payload, from screen to network process: (%s)", payload, 'start_client')
        networkProcess.input_queue.put(payload)

        # ask for 60 frames per second
        clock.tick(60)

    networkProcess.stop()
    game.quit()
