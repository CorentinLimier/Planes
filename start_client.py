
import pygame
from game.engine.engine import Game
from game.bo.player import Player
from network.client import ClientProcessTwisted as ClientProcess
from userInputFeed.userInputFeedLocal import UserInputFeedLocal
from userInput.userInput import UserInput
import socket
import json
import time


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
        #print "user_input -> payload: %s" % user_input
        payload = {}
        payload['has_pressed_left'] = user_input.has_pressed_left
        payload['has_pressed_right'] = user_input.has_pressed_right
        return payload

    def payload_to_user_input(payload):
        print "payload -> user_input: (%s)" % payload
        user_input = UserInput()
        user_input.has_pressed_left = payload['content']['has_pressed_left']
        user_input.has_pressed_right = payload['content']['has_pressed_right']
        return user_input


    quit = False
    while not quit:
        # fetch network inputs and update game state
        if not networkProcess.output_queue.empty():
            payload = networkProcess.output_queue.get()
            print 'output_queue from main (from server to app)'
            print payload

            if payload and 'type' in payload and payload['type'] == 'user_input':
                user_input = payload_to_user_input(payload)
                networkPlayer.update_state(user_input)
                print networkPlayer

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
        payload = user_input_to_payload(user_input)
        print 'input_queue from main (from server to app)'
        print payload
        networkProcess.input_queue.put(payload)

        # ask for 60 frames per second
        clock.tick(60)

    networkProcess.stop()
    game.quit()
