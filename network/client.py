
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
import multiprocessing
import sys
import os
from twisted.internet import reactor
import socket
import json


class ClientProtocol(LineReceiver):

    def rawDataReceived(self, data):
       LineReceiver.rawDataReceived(self, data)

    def __init__(self, on_new_line_callback):
        self.on_new_line_callback = on_new_line_callback

    def lineReceived(self, line):
        self.on_new_line_callback(line)


class ClientFactory(ClientFactory):
    def __init__(self, on_new_line_callback):
        self.on_new_line_callback = on_new_line_callback

    def buildProtocol(self, addr):
        return ClientProtocol(self.on_new_line_callback)


class ClientProcessTwisted(multiprocessing.Process):

    def __init__(self):
        # must call this before anything else
        multiprocessing.Process.__init__(self)
        self.output_queue = multiprocessing.Queue()
        self.input_queue = multiprocessing.Queue()
        self.name = 'network_input_feed'

    # this only method runs in a separate process
    def run(self):
        sys.stdout.write('[%s] running ...  process id: %s\n' % (self.name, os.getpid()))

        reactor.connectTCP('127.0.0.1', 5000, ClientFactory(self.new_line_received))
        reactor.run()

    def new_line_received(self, new_line):
        sys.stdout.write('[%s] new line received: %s\n' % (self.name, new_line))
        if new_line == 'quit':
            reactor.callFromThread(reactor.stop)

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


class ClientProcessSocket(multiprocessing.Process):

    def __init__(self):
        # must call this before anything else
        multiprocessing.Process.__init__(self)
        self.output_queue = multiprocessing.Queue()
        self.input_queue = multiprocessing.Queue()
        self.name = 'network_input_feed'
        self.socket = None
        self.server_address = ('127.0.0.1', 5000)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.setblocking(0)
        self.terminator = '\r\n'

    def __del__(self):
        self.socket.close()

    # this only method runs in a separate process
    def run(self):
        sys.stdout.write('[%s] running ...  process id: %s\n' % (self.name, os.getpid()))

        self.socket.connect(self.server_address)

        quit = False
        while not quit:
            json_payloads = ''
            try:
                json_payloads = self.socket.recv(1024)
            except socket.error:
                # no data yet
                pass

            json_payloads.replace(self.terminator, '')
            for json_payload in json_payloads.split('\n'):
                json_payload = json_payload.strip('\r')
                if json_payload == 'quit':
                    quit = True
                sys.stdout.write('[%s] IN payload "%s" client pid: %s\n' % (self.name, json_payload, os.getpid()))
                if json_payload != '':
                    payload = json.loads(json_payload)
                    self.output_queue.put(payload)

            while not self.input_queue.empty():
                payload = self.input_queue.get()
                sys.stdout.write('[%s] OUT payload "%s" client pid: %s\n' % (self.name, json.dumps(payload), os.getpid()))
                sent = self.socket.send(json.dumps(payload) + self.terminator)
                if sent == 0:
                    raise RuntimeError("socket connection broken")

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