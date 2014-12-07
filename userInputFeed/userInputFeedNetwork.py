from userInput.userInput import UserInput
import multiprocessing
import sys
import random
import os


class UserInputFeedNetwork(multiprocessing.Process):

    def __init__(self):
        # must call this before anything else
        multiprocessing.Process.__init__(self)
        self.output_queue = multiprocessing.Queue()
        self.input_queue = multiprocessing.Queue()
        self.name = 'network_input_feed'

    # this only method runs in a separate process
    def run(self):
        sys.stdout.write('[%s] running ...  process id: %s\n' % (self.name, os.getpid()))

        done = False
        while not done:
            user_input = UserInput()

            if random.randint(0, 1) == 1:
                user_input.has_pressed_left = True
                user_input.orientation_delta = -5
            else:
                user_input.has_pressed_right = True
                user_input.orientation_delta = 5

            self.output_queue.put(user_input)
            # quit process on input queue not empty
            sys.stdout.write('[%s] tick ...  process id: %s\n\n' % (self.name, os.getpid()))
            if not self.input_queue.empty():
                sys.stdout.write('[%s] quit received ...  process id: %s\n\n' % (self.name, os.getpid()))
                done = True

        sys.stdout.write('[%s] input feed network end ...  process id: %s\n\n' % (self.name, os.getpid()))

    def fetch_user_input(self):
        user_input = self.output_queue.get()
        return user_input

    def start(self):
        print "UserInputFeedNetwork: start"
        multiprocessing.Process.start(self)

    def stop(self):
        print "UserInputFeedNetwork: stop"
        self.input_queue.put('quit')
        multiprocessing.Process.terminate(self)


