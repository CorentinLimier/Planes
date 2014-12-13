
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import multiprocessing
from twisted.internet import reactor
import json
from twisted.internet import threads
import time
from logger.logger import Logger


def send_to_server_recursive_threaded_loop(connection_handler):
    Logger.trace('loop from network process sender thread', category='client')

    while not connection_handler.input_queue.empty():
        payload = connection_handler.input_queue.get()
        Logger.debug('fetch input_queue from network process sender thread', payload, category='client')
        connection_handler.sendLine(json.dumps(payload))

    time.sleep(0.5)  # 500 ms
    # get our Deferred which will be called with the largeFibonnaciNumber result
    threads.deferToThread(send_to_server_recursive_threaded_loop, connection_handler)


class ClientConnectionHandler(LineReceiver):

    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.name = 'ClientConnectionHandler'
        self.terminator = '\r\n'

    def connectionMade(self):
        Logger.debug('connection made from network process', category='client')
        send_to_server_recursive_threaded_loop(self)

    def connectionLost(self, reason):
        Logger.debug('connection lost from network process', category='client')

    def lineReceived(self, json_payloads):
        Logger.trace('line received lost from network process: (%s)', json_payloads, category='client')
        json_payloads.replace(self.terminator, '')
        for json_payload in json_payloads.split('\n'):
            json_payload = json_payload.strip('\r')
            if json_payload != '':
                payload = json.loads(json_payload)
                self.output_queue.put(payload)

    def rawDataReceived(self, data):
        pass


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
        Logger.debug('process start from network process', category='client')

        reactor.connectTCP('127.0.0.1', 5000, ClientFactory(self.input_queue, self.output_queue))
        reactor.run()

    def fetch_user_input(self):
        user_input = self.output_queue.get()
        return user_input

    def start(self):
        Logger.debug('start command received from network process', category='client')
        multiprocessing.Process.start(self)

    def stop(self):
        Logger.debug('stop command received from network process', category='client')
        self.input_queue.put('quit')
        multiprocessing.Process.terminate(self)

