from userInput.userInput import UserInput
import pygame
import time


class UserInputFeedLocal():
    def __init__(self):
        self._user_input = UserInput()

    def fetch_user_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._user_input.has_pressed_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._user_input.has_pressed_left = True
                elif event.key == pygame.K_RIGHT:
                    self._user_input.has_pressed_right = True
                elif event.key == pygame.K_SPACE:
                    self._user_input.has_pressed_fire = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                    self._user_input = UserInput()

        now = time.time()
        self._user_input.now = now
        return self._user_input
