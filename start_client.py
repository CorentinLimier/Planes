
import pygame
from game.engine.engine import Game
from game.hmi.hmi import Hmi
from game.bo.player import Player
from network.client import ClientProcessTwisted as ClientProcess
from userInputFeed.userInputFeedLocal import UserInputFeedLocal
from userInput.userInput import UserInput
from logger.logger import Logger

if __name__ == "__main__":
    pygame.init()
    game = Game()
    hmi = Hmi(800,400)
    clock = pygame.time.Clock()

    # init network process
    networkProcess = ClientProcess()
    networkProcess.start()

    # init local game
    localInputFeed = UserInputFeedLocal()
    game.init()

    # init local player
    localPlayerId = None
    localPlayer = Player(game, hmi)
    game.add_player(localPlayer)
    hmi.add_player(localPlayer)

    # init player map
    playerMap = {}

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
                user_id = payload['id']
                playerMap[user_id].update_state(user_input)

            if payload and 'type' in payload and payload['type'] == 'authentication':
                Logger.info("Authentication (%s)", payload, 'start_client')
                localPlayerId = payload['id']
                playerMap[localPlayerId] = localPlayer

            if payload and 'type' in payload and payload['type'] == 'user_list':
                Logger.info("User list (%s)", payload, 'start_client')
                for user_id in payload['users']['ids']:
                    if not user_id == localPlayerId:
                        networkPlayer = Player(game, hmi)
                        hmi.add_player(networkPlayer)
                        game.add_player(networkPlayer)
                        playerMap[user_id] = networkPlayer

            if payload and 'type' in payload and payload['type'] == 'new_connection':
                Logger.info("User new connection (%s)", payload, 'start_client')
                user_id = payload['id']
                networkPlayer = Player(game, hmi)
                hmi.add_player(networkPlayer)
                game.add_player(networkPlayer)
                playerMap[user_id] = networkPlayer

            if payload and 'type' in payload and payload['type'] == 'lost_connection':
                Logger.info("User lost connection (%s)", payload, 'start_client')
                user_id = payload['id']
                networkPlayer = playerMap[user_id]
                hmi.remove_player(networkPlayer)
                game.remove_player(networkPlayer)
                playerMap.pop(user_id, None)


        # fetch local input and update game state
        user_input = localInputFeed.fetch_user_input()
        localPlayer.update_state(user_input)

        # redraw game
        hmi.draw()

        if user_input.has_pressed_something():
            # send local user_inputs
            Logger.debug("user_input to payload, from screen to network process", category='start_client')
            payload = user_input_to_payload(user_input)
            Logger.trace("user_input to payload, from screen to network process: (%s)", payload, 'start_client')
            networkProcess.input_queue.put(payload)

        # ask for 60 frames per second
        clock.tick(60)

    networkProcess.stop()
    game.quit()
