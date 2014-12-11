
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import multiprocessing
import sys
import os
from twisted.internet import reactor
import json
from twisted.internet import threads
import time


def send_to_server_recursive_threaded_loop(connection_handler):
    sys.stdout.write('[?:%s] looping: sendToServerRecursiveThreadedLoop\n' % (os.getpid()))

    while not connection_handler.input_queue.empty():
        payload = connection_handler.input_queue.get()
        sys.stdout.write('[?:%s] OUT payload (from app to server) "%s"\n' % (os.getpid(), payload))
        connection_handler.sendLine(json.dumps(payload))

    time.sleep(0.5)  # 500 ms
    # get our Deferred which will be called with the largeFibonnaciNumber result
    d = threads.deferToThread(send_to_server_recursive_threaded_loop, connection_handler)
    # add our callback to print it out
    d.addCallback(send_to_server_recursive_threaded_loop_callback)


def send_to_server_recursive_threaded_loop_callback(result):
    sys.stdout.write('[?:%s] loop iteration: callback called sendToServerRecursiveThreadedLoopCallback ("%s")\n' % (os.getpid(), result))


class ClientConnectionHandler(LineReceiver):

    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.name = 'ClientConnectionHandler'
        self.terminator = '\r\n'

    def connectionMade(self):
        sys.stdout.write('[%s:%s] twisted connection made\n' % (self.name, os.getpid()))
        send_to_server_recursive_threaded_loop(self)

    def connectionLost(self, reason):
        sys.stdout.write('[%s:%s] twisted connection lost\n' % (self.name, os.getpid()))

    def lineReceived(self, json_payloads):
        sys.stdout.write('[%s:%s] twisted line received "%s"\n' % (self.name, os.getpid(), json_payloads))
        json_payloads.replace(self.terminator, '')
        for json_payload in json_payloads.split('\n'):
            json_payload = json_payload.strip('\r')
            if json_payload != '':
                payload = json.loads(json_payload)
                self.output_queue.put(payload)

    def rawDataReceived(self, data):
        sys.stdout.write('[%s:%s] twisted raw data received "%s"\n' % (self.name, os.getpid(), line))


class ClientFactory(ClientFactory):

    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue

    def buildProtocol(self, address):
        return ClientConnectionHandler(self.input_queue, self.output_queue)


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

        reactor.connectTCP('127.0.0.1', 5000, ClientFactory(self.input_queue, self.output_queue))
        reactor.run()

    def fetch_user_input(self):
        user_input = self.output_queue.get()
        return user_input

    def start(self):
        sys.stdout.write('[%s:%s] started\n' % (self.name, os.getpid()))
        multiprocessing.Process.start(self)

    def stop(self):
        sys.stdout.write('[%s:%s] stopped\n' % (self.name, os.getpid()))
        self.input_queue.put('quit')
        multiprocessing.Process.terminate(self)

