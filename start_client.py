
import pygame
from game.engine.engine import Game
from game.hmi.hmi import Hmi
from game.network.protocol import UserInputDataUnit
from network.client import ClientProcessTwisted as ClientProcess
from userInputFeed.userInputFeedLocal import UserInputFeedLocal
from logger.logger import Logger

if __name__ == "__main__":
    pygame.init()
    game = Game(800, 400)
    hmi = Hmi(game)
    clock = pygame.time.Clock()

    # init network process
    networkProcess = ClientProcess()
    networkProcess.start()

    # init local game
    localInputFeed = UserInputFeedLocal()
    game.init()

    # init local player
    localPlayerId = None
    localPlayer = game.add_player()

    # init player map
    playerMap = {}

    quit_the_game = False
    while not quit_the_game:
        # fetch network inputs and update game state
        if not networkProcess.output_queue.empty():
            payload = networkProcess.output_queue.get()
            Logger.debug("fetch input_queue from main, from network process to screen", category='start_client')

            if payload and 'type' in payload:
                if payload['type'] == 'user_input':
                    Logger.trace("fetch input_queue from main, from network process to screen: (%s)", payload, 'start_client')
                    user_input = UserInputDataUnit(payload['content']).get_object()
                    user_id = payload['user']['id']
                    game.update_player(playerMap[user_id], user_input)

                elif payload['type'] == 'authentication':
                    Logger.info("Authentication (%s)", payload, 'start_client')
                    localPlayerId = payload['user']['id']
                    playerMap[localPlayerId] = localPlayer

                elif payload['type'] == 'user_list':
                    Logger.info("User list (%s)", payload, 'start_client')
                    for user_pdu in payload['users']:
                        if not user_pdu['id'] == localPlayerId:
                            networkPlayer = game.add_player()
                            playerMap[user_pdu['id']] = networkPlayer

                elif payload['type'] == 'new_connection':
                    Logger.info("User new connection (%s)", payload, 'start_client')
                    user_id = payload['user']['id']
                    networkPlayer = game.add_player()
                    playerMap[user_id] = networkPlayer

                elif payload['type'] == 'lost_connection':
                    Logger.info("User lost connection (%s)", payload, 'start_client')
                    user_id = payload['id']
                    game.remove_player(playerMap[user_id])
                    playerMap.pop(user_id, None)

                else:
                    Logger.error('Unknown payload type: (%s)', payload['type'], 'start_client')

            else:
                Logger.error('Payload not defined or "type" key not defined: %s', payload, 'start_client')

        # fetch local input and update game state
        user_input = localInputFeed.fetch_user_input()
        game.update_player(localPlayer, user_input)

        # redraw game
        game.tick()
        hmi.draw()

        if user_input.has_pressed_something():
            # send local user_inputs
            Logger.debug("user_input to payload, from screen to network process", category='start_client')
            payload = {
                'type': 'user_input',
                'content': UserInputDataUnit(user_input).get_pdu()
            }
            Logger.trace("user_input to payload, from screen to network process: (%s)", payload, 'start_client')
            networkProcess.input_queue.put(payload)

        # ask for 60 frames per second
        clock.tick(60)

    networkProcess.stop()
    game.quit()
